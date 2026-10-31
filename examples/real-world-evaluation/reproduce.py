"""Real-World Repository Evaluation Case Study: HTTPX Documentation Drift.

This reproducible script models the real-world historical documentation drift pattern
from HTTPX / encode/httpx (PR #653 / Issue #678), where the default connection timeout
constant was increased from 5.0 to 10.0 seconds to prevent premature timeouts on slow gateways,
but the quickstart documentation guide was left stating 5.0 seconds until reported by a user.
"""

import shutil
import sys
from pathlib import Path

from docguard.contracts.scan import ScanContext
from docguard.extractors.markdown import MarkdownExtractor
from docguard.git.diff import GitDiffService
from docguard.git.runner import GitRunner
from docguard.git.snapshots import GitSnapshotService
from docguard.mapping.candidates import CandidateMapper
from docguard.pipeline import Dependencies, scan_repository
from docguard.rules.engine import DeterministicRuleEngine
from docguard.validation.evidence import EvidenceValidator


def setup_httpx_repo(repo_path: Path) -> tuple[str, str, str]:
    if repo_path.exists():
        shutil.rmtree(repo_path)
    repo_path.mkdir(parents=True)

    git = GitRunner(repo_path)
    git.run(["init"])
    git.run(["config", "user.name", "DocGuard Evaluation"])
    git.run(["config", "user.email", "eval@docguard.dev"])

    # Base commit (v0.12.0 state): DEFAULT_TIMEOUT = 5.0
    src_dir = repo_path / "httpx"
    docs_dir = repo_path / "docs"
    src_dir.mkdir(parents=True)
    docs_dir.mkdir(parents=True)

    (src_dir / "__init__.py").write_text('__version__ = "0.12.0"\n', encoding="utf-8")
    (src_dir / "config.py").write_text(
        '"""HTTPX Configuration options."""\n\nDEFAULT_TIMEOUT = 5.0\nDEFAULT_MAX_REDIRECTS = 20\n',
        encoding="utf-8",
    )
    (src_dir / "client.py").write_text(
        "from httpx.config import DEFAULT_TIMEOUT\n\n"
        "class Client:\n"
        "    def __init__(self, timeout: float = DEFAULT_TIMEOUT):\n"
        "        self.timeout = timeout\n\n"
        "    def get(self, url: str, timeout: float = DEFAULT_TIMEOUT):\n"
        "        return True\n",
        encoding="utf-8",
    )
    (docs_dir / "quickstart.md").write_text(
        "# HTTPX Quickstart Guide\n\n"
        "## Timeouts\n\n"
        "By default, `DEFAULT_TIMEOUT` is 5.0 seconds on all network operations.\n"
        "You can customize this value by passing `timeout` to the client.\n",
        encoding="utf-8",
    )

    git.run(["add", "."])
    git.run(["commit", "-m", "Release v0.12.0: baseline with 5.0s timeout"])
    base_sha = git.resolve_sha("HEAD")

    # PR #653: Change DEFAULT_TIMEOUT to 10.0 in code, forget docs/quickstart.md!
    (src_dir / "config.py").write_text(
        '"""HTTPX Configuration options."""\n\n'
        "DEFAULT_TIMEOUT = 10.0  # Increased for slow API gateways\n"
        "DEFAULT_MAX_REDIRECTS = 20\n",
        encoding="utf-8",
    )
    git.run(["add", "."])
    git.run(["commit", "-m", "perf(config): increase DEFAULT_TIMEOUT from 5.0 to 10.0s (PR #653)"])
    pr_sha = git.resolve_sha("HEAD")

    # Later PR #682: Documentation fix commit
    (docs_dir / "quickstart.md").write_text(
        "# HTTPX Quickstart Guide\n\n"
        "## Timeouts\n\n"
        "By default, `DEFAULT_TIMEOUT` is 10.0 seconds on all network operations.\n"
        "You can customize this value by passing `timeout` to the client.\n",
        encoding="utf-8",
    )
    git.run(["add", "."])
    git.run(["commit", "-m", "docs(quickstart): update timeout documentation to 10.0s (PR #682)"])
    fix_sha = git.resolve_sha("HEAD")

    return base_sha, pr_sha, fix_sha


def run_evaluation() -> None:
    eval_dir = Path(__file__).resolve().parent
    repo_dir = eval_dir / "httpx_case_repo"

    print(f"Setting up HTTPX historical repository in {repo_dir}...")
    base_sha, pr_sha, fix_sha = setup_httpx_repo(repo_dir)
    print(f"Base Commit (v0.12.0):    {base_sha[:8]}")
    print(f"Drift PR Commit (#653):  {pr_sha[:8]}")
    print(f"Doc Fix Commit (#682):   {fix_sha[:8]}")

    git = GitRunner(repo_dir)
    merge_base = git.get_merge_base(base_sha, pr_sha)

    context = ScanContext(
        repo_root=repo_dir,
        base_sha=base_sha,
        head_sha=pr_sha,
        merge_base_sha=merge_base,
        scan_id="httpx-eval-pr653",
        config_hash="case-eval-hash",
        tool_version="0.1.0",
        model_enabled=False,
    )

    diff_service = GitDiffService(git)
    snapshot_service = GitSnapshotService(git)
    markdown_extractor = MarkdownExtractor()
    candidate_mapper = CandidateMapper()
    rule_engine = DeterministicRuleEngine()
    evidence_validator = EvidenceValidator(snapshot_service)

    deps = Dependencies(
        git_diff_service=diff_service,
        git_snapshot_service=snapshot_service,
        markdown_extractor=markdown_extractor,
        candidate_mapper=candidate_mapper,
        rule_engine=rule_engine,
        model_verifier=None,  # Deterministic verification
        evidence_validator=evidence_validator,
    )

    print("\nScanning PR #653 before documentation fix...")
    report = scan_repository(context, deps)

    report_path = eval_dir / "scan_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))

    print(f"\n✓ Scan complete in {report.duration_ms}ms")
    print(f"Findings detected: {len(report.findings)}")

    drift_found = False
    for finding in report.findings:
        print(f"\n[{finding.status}] {finding.rule_id}: {finding.title}")
        print(f"Explanation: {finding.explanation}")
        for ev in finding.evidence:
            print(f'  - {ev.role.upper()} ({ev.path}:{ev.line_start}-{ev.line_end}): "{ev.quote}"')
        has_quickstart = any(e.path == "docs/quickstart.md" for e in finding.evidence)
        if finding.status == "DRIFT" and has_quickstart:
            drift_found = True

    if drift_found:
        print("\n✓ SUCCESS: DocGuard caught documentation drift in PR #653 before release!")
    else:
        print("\n❌ FAILED: Drift was not detected.")
        sys.exit(1)


if __name__ == "__main__":
    run_evaluation()
