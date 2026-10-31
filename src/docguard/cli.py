import json
from pathlib import Path

import typer
from rich.console import Console

from docguard import __version__
from docguard.contracts.findings import ScanReport

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
    console.print("[bold green]DocGuard[/bold green] starting scan...")
    console.print(f"Scanning {repo} from [yellow]{base}[/yellow] to [cyan]{head}[/cyan]")


@app.command(name="replay")
def replay_command(
    manifest: Path = typer.Option(
        ...,
        "--manifest",
        "-m",
        help="Path to replay manifest JSON.",
        exists=True,
    ),
) -> None:
    """Run historical replay evaluation against a manifest of known changes."""
    console.print(f"Loading replay manifest from {manifest}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
