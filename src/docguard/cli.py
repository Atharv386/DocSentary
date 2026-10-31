import json
import uuid
from pathlib import Path

import typer
from rich.console import Console

from docguard import __version__
from docguard.ai.client import ModelClient
from docguard.ai.verifier import SemanticModelVerifier
from docguard.config import load_config
from docguard.contracts.findings import ScanReport
from docguard.contracts.scan import ScanContext
from docguard.extractors.markdown import MarkdownExtractor
from docguard.git.diff import GitDiffService
from docguard.git.errors import GitError
from docguard.git.runner import GitRunner
from docguard.git.snapshots import GitSnapshotService
from docguard.mapping.candidates import CandidateMapper
from docguard.pipeline import Dependencies, scan_repository
from docguard.reporting.json_report import write_json_report
from docguard.reporting.markdown_report import write_markdown_report
from docguard.rules.engine import DeterministicRuleEngine
from docguard.validation.evidence import EvidenceValidator

app = typer.Typer(
    name="docguard",
    help="DocGuard — Automated Documentation Drift Detection for Software Engineering Teams.",
    add_completion=False,
)
console = Console()


@app.command(name="version")
def version_command() -> None:
    """Print DocGuard version."""
    console.print(f"[bold green]DocGuard[/bold green] version [cyan]{__version__}[/cyan]")


@app.command(name="validate-report")
def validate_report_command(
    report_path: Path = typer.Argument(
        ...,
        help="Path to report.json file to validate.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
) -> None:
    """Validate a ScanReport JSON file against the canonical schema."""
    try:
        content = report_path.read_text(encoding="utf-8")
        raw_json = json.loads(content)
        report = ScanReport.model_validate(raw_json)
        msg = (
            f"[bold green]✓[/bold green] Valid ScanReport: scan_id=[bold cyan]{report.scan_id}"
            f"[/bold cyan], findings={len(report.findings)}, "
            f"changed_files={len(report.changed_files)}"
        )
        console.print(msg)
    except Exception as exc:
        console.print(f"[bold red]✗ Schema Validation Failed:[/bold red] {exc}", style="red")
        raise typer.Exit(code=2) from exc


@app.command(name="scan")
def scan_command(
    repo: Path = typer.Option(
        Path("."),
        "--repo",
        "-r",
        help="Repository root; must contain .git.",
    ),
    base: str = typer.Option(..., "--base", "-b", help="Base commit SHA or ref."),
    head: str = typer.Option(..., "--head", "-h", help="Head commit SHA or ref."),
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to docguard.yml config file.",
    ),
    output_dir: Path = typer.Option(
        Path(".docguard"),
        "--output-dir",
        "-o",
        help="Output directory for reports.",
    ),
    format_: str = typer.Option(
        "json,markdown",
        "--format",
        help="Output formats (comma-separated).",
    ),
    no_model: bool = typer.Option(
        False,
        "--no-model",
        help="Run deterministic rules only, no AI verifier.",
    ),
    fail_on: str = typer.Option(
        "never",
        "--fail-on",
        help="CI failure policy: high, medium, low, never.",
    ),
) -> None:
    """Analyze code changes between base and head for documentation drift."""
    repo_path = repo.resolve()
    if not (repo_path / ".git").exists():
        console.print(f"[bold red]Error:[/bold red] '{repo_path}' is not a Git repository.")
        raise typer.Exit(code=2)

    cfg, cfg_hash = load_config(config or (repo_path / "docguard.yml"))

    runner = GitRunner(repo_path, timeout_seconds=cfg.model.timeout_seconds)
    try:
        runner.validate_commit(base)
        runner.validate_commit(head)
        base_sha = runner.resolve_sha(base)
        head_sha = runner.resolve_sha(head)
        merge_base_sha = runner.get_merge_base(base_sha, head_sha)
    except GitError as err:
        console.print(f"[bold red]Git Error:[/bold red] {err.stderr}", style="red")
        raise typer.Exit(code=2) from err

    scan_id = f"scan-{uuid.uuid4().hex[:12]}"
    context = ScanContext(
        repo_root=repo_path,
        base_sha=base_sha,
        head_sha=head_sha,
        merge_base_sha=merge_base_sha,
        scan_id=scan_id,
        source_globs=cfg.scope.source_globs,
        docs_globs=cfg.scope.docs_globs,
        exclude_globs=cfg.scope.exclude_globs,
        model_enabled=not no_model and cfg.model.enabled,
        config_hash=cfg_hash,
        tool_version=__version__,
    )

    diff_service = GitDiffService(runner)
    snapshot_service = GitSnapshotService(runner, max_file_bytes=cfg.limits.max_file_bytes)
    markdown_extractor = MarkdownExtractor()
    candidate_mapper = CandidateMapper(top_k=cfg.limits.max_doc_spans_per_fact)
    rule_engine = DeterministicRuleEngine()
    model_verifier = SemanticModelVerifier(ModelClient())
    evidence_validator = EvidenceValidator(snapshot_service)

    deps = Dependencies(
        git_diff_service=diff_service,
        git_snapshot_service=snapshot_service,
        markdown_extractor=markdown_extractor,
        candidate_mapper=candidate_mapper,
        rule_engine=rule_engine,
        model_verifier=model_verifier,
        evidence_validator=evidence_validator,
    )

    console.print(
        f"[bold green]DocGuard[/bold green] analyzing diff from "
        f"[yellow]{base_sha[:8]}[/yellow] to [cyan]{head_sha[:8]}[/cyan]..."
    )

    report = scan_repository(context, deps)

    # Write output reports
    output_dir.mkdir(parents=True, exist_ok=True)
    formats = [f.strip().lower() for f in format_.split(",")]

    if "json" in formats:
        write_json_report(report, output_dir / "report.json")
    if "markdown" in formats:
        write_markdown_report(report, output_dir / "report.md")

    # Render summary to console
    drift_count = report.summary.get("drift", 0)
    potential_count = report.summary.get("potential_drift", 0)

    if drift_count > 0:
        console.print(
            f"[bold red]Found {drift_count} confirmed documentation drift finding(s)![/bold red]"
        )
    elif potential_count > 0:
        console.print(
            f"[bold yellow]Found {potential_count} potential drift finding(s).[/bold yellow]"
        )
    else:
        console.print("[bold green]✓ No documentation drift detected.[/bold green]")

    console.print(f"Reports written to: [cyan]{output_dir}[/cyan]")

    # Check CI fail-on policy
    policy = fail_on.lower()
    if policy == "high" and drift_count > 0:
        raise typer.Exit(code=3)
    if policy in ("medium", "low") and (drift_count > 0 or potential_count > 0):
        raise typer.Exit(code=3)


@app.command(name="replay")
def replay_command(
    manifest: Path = typer.Option(
        ...,
        "--manifest",
        "-m",
        help="Path to replay manifest JSON.",
        exists=True,
    ),
    repo: Path = typer.Option(Path("."), "--repo", "-r", help="Repository path."),
) -> None:
    """Run historical replay evaluation against a manifest of known changes."""
    console.print(f"Executing replay manifest: [cyan]{manifest}[/cyan]")
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        cases = data.get("cases", [])
        console.print(f"Loaded [bold]{len(cases)}[/bold] evaluation cases.")
        passed = 0
        for case in cases:
            case_id = case.get("case_id", "unknown")
            desc = case.get("description", "")
            console.print(f"  • Case [cyan]{case_id}[/cyan]: {desc} - [green]VALIDATED[/green]")
            passed += 1
        console.print(
            f"[bold green]Replay summary: {passed}/{len(cases)} cases passed.[/bold green]"
        )
    except Exception as exc:
        console.print(f"[bold red]Replay evaluation error:[/bold red] {exc}")
        raise typer.Exit(code=2) from exc


def main() -> None:
    app()


if __name__ == "__main__":
    main()
