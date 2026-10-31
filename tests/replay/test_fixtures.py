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
from docsentry.rules.engine import DeterministicRuleEngine
from docsentry.validation.evidence import EvidenceValidator


def _build_and_scan(repo_path: Path, files_base: dict[str, str], files_head: dict[str, str]):
    runner = GitRunner(repo_path)
    runner.run(["init"])
    runner.run(["config", "user.name", "DocGuard Replay"])
    runner.run(["config", "user.email", "replay@docsentry.local"])

    for path_str, content in files_base.items():
        f = repo_path / path_str
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")

    runner.run(["add", "."])
    runner.run(["commit", "-m", "Base commit"])
    base_sha = runner.resolve_sha("HEAD")

    for path_str, content in files_head.items():
        f = repo_path / path_str
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")

    runner.run(["add", "."])
    runner.run(["commit", "-m", "Head commit"])
    head_sha = runner.resolve_sha("HEAD")
    merge_base = runner.get_merge_base(base_sha, head_sha)

    ctx = ScanContext(
        repo_root=repo_path,
        base_sha=base_sha,
        head_sha=head_sha,
        merge_base_sha=merge_base,
        scan_id="replay-test",
        model_enabled=False,
        config_hash="replayhash",
        tool_version=__version__,
    )

    diff_service = GitDiffService(runner)
    snapshot_service = GitSnapshotService(runner)
    deps = Dependencies(
        git_diff_service=diff_service,
        git_snapshot_service=snapshot_service,
        markdown_extractor=MarkdownExtractor(),
        candidate_mapper=CandidateMapper(),
        rule_engine=DeterministicRuleEngine(),
        model_verifier=SemanticModelVerifier(ModelClient()),
        evidence_validator=EvidenceValidator(snapshot_service),
    )

    return scan_repository(ctx, deps)


def test_f01_stale_default(tmp_path: Path) -> None:
    base = {
        "src/client.py": "def connect(timeout=30):\n    pass\n",
        "docs/config.md": "# Config\nThe default timeout is 30 seconds.\n",
    }
    head = {
        "src/client.py": "def connect(timeout=60):\n    pass\n",
        "docs/config.md": "# Config\nThe default timeout is 30 seconds.\n",
    }
    report = _build_and_scan(tmp_path, base, head)
    assert report.summary["drift"] == 1
    assert report.findings[0].rule_id == "PY-DEFAULT-001"


def test_f02_parameter_added(tmp_path: Path) -> None:
    base = {
        "src/client.py": "def connect(host, port=80):\n    pass\n",
        "docs/api.md": "# API\nConnect to host with `connect(host, port)`.\n",
    }
    head = {
        "src/client.py": "def connect(host, port=80, retries=3):\n    pass\n",
        "docs/api.md": "# API\nConnect to host with `connect(host, port)`.\n",
    }
    report = _build_and_scan(tmp_path, base, head)
    # The new parameter is added; no stale default flagged
    assert report.summary["drift"] == 0


def test_f03_removed_symbol(tmp_path: Path) -> None:
    base = {
        "src/auth.py": "def old_login():\n    return True\n",
        "docs/tutorial.md": "# Tutorial\nCall `old_login` to authenticate.\n",
    }
    head = {
        "src/auth.py": "def modern_login():\n    return True\n",
        "docs/tutorial.md": "# Tutorial\nCall `old_login` to authenticate.\n",
    }
    report = _build_and_scan(tmp_path, base, head)
    assert report.summary["potential_drift"] == 1
    assert report.findings[0].rule_id == "PY-SYMBOL-003"


def test_f04_renamed_flag(tmp_path: Path) -> None:
    base = {
        "src/cli.py": (
            "import argparse\np = argparse.ArgumentParser()\np.add_argument('--timeout')\n"
        ),
        "docs/flags.md": "# CLI Flags\n`--timeout` specifies connection timeout.\n",
    }
    head = {
        "src/cli.py": (
            "import argparse\np = argparse.ArgumentParser()\np.add_argument('--request-timeout')\n"
        ),
        "docs/flags.md": "# CLI Flags\n`--timeout` specifies connection timeout.\n",
    }
    report = _build_and_scan(tmp_path, base, head)
    assert report.summary["drift"] == 1
    assert report.findings[0].rule_id == "PY-CONFIG-004"


def test_f05_no_doc_impact(tmp_path: Path) -> None:
    base = {
        "src/internal.py": "def _compute_hash(data):\n    x = 1\n    return x\n",
        "docs/guide.md": "# Guide\nOur system securely processes records.\n",
    }
    head = {
        "src/internal.py": (
            "def _compute_hash(data):\n    optimized_x = 2\n    return optimized_x\n"
        ),
        "docs/guide.md": "# Guide\nOur system securely processes records.\n",
    }
    report = _build_and_scan(tmp_path, base, head)
    assert report.summary["findings"] == 0


def test_f06_docs_fixed_same_pr(tmp_path: Path) -> None:
    base = {
        "src/client.py": "def connect(timeout=30):\n    pass\n",
        "docs/config.md": "# Config\nThe default timeout is 30 seconds.\n",
    }
    head = {
        "src/client.py": "def connect(timeout=60):\n    pass\n",
        "docs/config.md": "# Config\nThe default timeout is 60 seconds.\n",
    }
    report = _build_and_scan(tmp_path, base, head)
    assert report.summary["findings"] == 0
