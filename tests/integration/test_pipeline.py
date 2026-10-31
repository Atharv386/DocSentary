from pathlib import Path

from docsentry import __version__
from docsentry.ai.client import ModelClient
from docsentry.ai.verifier import SemanticModelVerifier
from docsentry.contracts.scan import ScanContext
from docsentry.extractors.markdown import MarkdownExtractor
from docsentry.git.diff import GitDiffService
from docsentry.git.runner import GitRunner
from docsentry.git.snapshots import GitSnapshotService
from docsentry.mapping.candidates import CandidateMapper
from docsentry.pipeline import Dependencies, scan_repository
from docsentry.reporting.markdown_report import render_markdown_report
from docsentry.rules.engine import DeterministicRuleEngine
from docsentry.validation.evidence import EvidenceValidator


def test_end_to_end_drift_detection(tmp_path: Path) -> None:
    # 1. Setup git repo
    runner = GitRunner(tmp_path)
    runner.run(["init"])
    runner.run(["config", "user.name", "DocGuard CI"])
    runner.run(["config", "user.email", "ci@docsentry.local"])

    # Base commit: client.py with timeout=30
    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)
    client_py = src_dir / "client.py"
    client_py.write_text("def connect(timeout=30):\n    return True\n", encoding="utf-8")

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(parents=True)
    config_md = docs_dir / "config.md"
    config_md.write_text(
        "# Configuration\n\n## Networking\nThe default timeout is 30 seconds.\n",
        encoding="utf-8",
    )

    runner.run(["add", "."])
    runner.run(["commit", "-m", "Initial commit"])
    base_sha = runner.resolve_sha("HEAD")

    # Head commit: change timeout to 60 in code, but docs remain 30
    client_py.write_text("def connect(timeout=60):\n    return True\n", encoding="utf-8")
    runner.run(["add", "."])
    runner.run(["commit", "-m", "Update timeout default to 60"])
    head_sha = runner.resolve_sha("HEAD")

    merge_base = runner.get_merge_base(base_sha, head_sha)

    # 2. Configure DocGuard scan
    ctx = ScanContext(
        repo_root=tmp_path,
        base_sha=base_sha,
        head_sha=head_sha,
        merge_base_sha=merge_base,
        scan_id="test-scan-e2e",
        model_enabled=False,
        config_hash="testhash",
        tool_version=__version__,
    )

    diff_service = GitDiffService(runner)
    snapshot_service = GitSnapshotService(runner)
    markdown_extractor = MarkdownExtractor()
    candidate_mapper = CandidateMapper()
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

    # 3. Execute scan
    report = scan_repository(ctx, deps)

    # 4. Assert findings
    assert report.scan_id == "test-scan-e2e"
    assert report.summary["drift"] == 1
    assert len(report.findings) == 1

    finding = report.findings[0]
    assert finding.status == "DRIFT"
    assert finding.rule_id == "PY-DEFAULT-001"
    assert finding.category == "default_value_mismatch"
    assert len(finding.evidence) == 2

    # Check evidence details
    code_ev = next(e for e in finding.evidence if e.role == "code")
    doc_ev = next(e for e in finding.evidence if e.role == "documentation")

    assert code_ev.path == "src/client.py"
    assert "timeout=60" in code_ev.quote

    assert doc_ev.path == "docs/config.md"
    assert "30 seconds" in doc_ev.quote

    # 5. Assert markdown render
    md_output = render_markdown_report(report)
    assert "# DocGuard Analysis Report" in md_output
    assert "1 Confirmed Drift" in md_output
    assert "PY-DEFAULT-001" in md_output
    assert "Documentation (Outdated Statement)" in md_output
