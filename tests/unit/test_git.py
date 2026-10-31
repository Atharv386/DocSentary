from pathlib import Path

import pytest

from docguard.git.diff import GitDiffService, parse_name_status_z, parse_unified_diff
from docguard.git.errors import GitError
from docguard.git.runner import GitRunner
from docguard.git.snapshots import GitSnapshotService


def test_parse_name_status_z() -> None:
    # A\0file1.py\0M\0file2.py\0R100\0old.py\0new.py\0D\0file3.py\0
    raw = "A\0file1.py\0M\0file2.py\0R100\0old.py\0new.py\0D\0file3.py\0"
    entries = parse_name_status_z(raw)
    assert len(entries) == 4
    assert entries[0] == ("A", "file1.py", None)
    assert entries[1] == ("M", "file2.py", None)
    assert entries[2] == ("R", "old.py", "new.py")
    assert entries[3] == ("D", "file3.py", None)


def test_parse_unified_diff() -> None:
    diff_text = """diff --git a/src/client.py b/src/client.py
index abc..def 100644
--- a/src/client.py
+++ b/src/client.py
@@ -10,3 +10,3 @@ def connect():
-def connect(timeout=30):
+def connect(timeout=60):
     pass
"""
    hunks = parse_unified_diff(diff_text)
    assert "src/client.py" in hunks
    assert len(hunks["src/client.py"]) == 1
    hunk = hunks["src/client.py"][0]
    assert hunk.old_start == 10
    assert hunk.new_start == 10
    assert hunk.removed_lines == ["def connect(timeout=30):"]
    assert hunk.added_lines == ["def connect(timeout=60):"]


def test_git_service_with_temp_repo(tmp_path: Path) -> None:
    runner = GitRunner(tmp_path)
    # Initialize git repo in tmp_path
    runner.run(["init"])
    runner.run(["config", "user.name", "DocGuard Test"])
    runner.run(["config", "user.email", "test@docguard.local"])

    # Commit 1 (base)
    file1 = tmp_path / "client.py"
    file1.write_text("def connect(timeout=30):\n    return True\n", encoding="utf-8")
    runner.run(["add", "client.py"])
    runner.run(["commit", "-m", "Initial commit"])
    base_sha = runner.resolve_sha("HEAD")

    # Create branch and Commit 2 (head)
    runner.run(["checkout", "-b", "feature"])
    file1.write_text("def connect(timeout=60):\n    return True\n", encoding="utf-8")
    doc_file = tmp_path / "config.md"
    doc_file.write_text("# Config\nThe default timeout is 30 seconds.\n", encoding="utf-8")
    runner.run(["add", "client.py", "config.md"])
    runner.run(["commit", "-m", "Change timeout to 60"])
    head_sha = runner.resolve_sha("HEAD")

    merge_base = runner.get_merge_base(base_sha, head_sha)
    assert merge_base == base_sha

    diff_service = GitDiffService(runner)
    changed = diff_service.get_changed_files(merge_base, head_sha)
    assert len(changed) == 2

    client_ch = next(c for c in changed if c.path_after == "client.py")
    assert client_ch.change_type == "modified"
    assert len(client_ch.hunks) == 1

    doc_ch = next(c for c in changed if c.path_after == "config.md")
    assert doc_ch.change_type == "added"

    snapshot_service = GitSnapshotService(runner)
    old_client = snapshot_service.read_file(base_sha, "client.py")
    assert old_client is not None
    assert "timeout=30" in old_client

    new_client = snapshot_service.read_file(head_sha, "client.py")
    assert new_client is not None
    assert "timeout=60" in new_client

    # Test path traversal prevention
    with pytest.raises(ValueError, match="Illegal path traversal"):
        snapshot_service.read_file(head_sha, "../secret.txt")


def test_missing_commit_raises_git_error(tmp_path: Path) -> None:
    runner = GitRunner(tmp_path)
    runner.run(["init"])
    with pytest.raises(GitError):
        runner.validate_commit("deadbeef" * 5)
