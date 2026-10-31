import re
from typing import Literal

from docguard.contracts.diff import ChangedFile, DiffHunk
from docguard.git.runner import GitRunner

HUNK_HEADER_RE = re.compile(
    r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@ ?(.*)$"
)


def parse_name_status_z(output: str) -> list[tuple[str, str, str | None]]:
    """
    Parses git diff --name-status -z output.
    Returns list of (status_code, path_primary, path_secondary_if_renamed).
    """
    if not output:
        return []

    tokens = output.split("\0")
    results: list[tuple[str, str, str | None]] = []
    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        if not token:
            idx += 1
            continue

        status_code = token[0]
        if status_code == "R":
            # Rename: token, old_path, new_path
            old_path = tokens[idx + 1]
            new_path = tokens[idx + 2]
            results.append((status_code, old_path, new_path))
            idx += 3
        else:
            path = tokens[idx + 1]
            results.append((status_code, path, None))
            idx += 2
    return results


def parse_unified_diff(diff_text: str) -> dict[str, list[DiffHunk]]:
    """
    Parses a unified diff into a mapping of file_path -> list of DiffHunk.
    """
    file_hunks: dict[str, list[DiffHunk]] = {}
    current_file: str | None = None
    current_hunk: DiffHunk | None = None

    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            current_hunk = None
            current_file = None
        elif line.startswith("+++ b/"):
            current_file = line[6:]
            if current_file not in file_hunks:
                file_hunks[current_file] = []
        elif line.startswith("@@ "):
            match = HUNK_HEADER_RE.match(line)
            if match and current_file:
                old_start = int(match.group(1))
                old_count = int(match.group(2)) if match.group(2) is not None else 1
                new_start = int(match.group(3))
                new_count = int(match.group(4)) if match.group(4) is not None else 1
                header = match.group(5) or None
                current_hunk = DiffHunk(
                    old_start=old_start,
                    old_count=old_count,
                    new_start=new_start,
                    new_count=new_count,
                    header=header,
                    added_lines=[],
                    removed_lines=[],
                )
                file_hunks[current_file].append(current_hunk)
        elif current_hunk is not None:
            if line.startswith("+") and not line.startswith("+++"):
                current_hunk.added_lines.append(line[1:])
            elif line.startswith("-") and not line.startswith("---"):
                current_hunk.removed_lines.append(line[1:])

    return file_hunks


class GitDiffService:
    """Computes changed files and diff hunks between merge base and head."""

    def __init__(self, runner: GitRunner) -> None:
        self.runner = runner

    def get_changed_files(self, merge_base_sha: str, head_sha: str) -> list[ChangedFile]:
        # Get raw name-status with NUL delimiter
        name_status_raw = self.runner.run(
            ["diff", "--name-status", "-z", "--find-renames", merge_base_sha, head_sha, "--"]
        )
        status_entries = parse_name_status_z(name_status_raw)

        # Get unified diff for hunk parsing
        unified_diff_raw = self.runner.run(
            [
                "diff",
                "--find-renames",
                "--no-ext-diff",
                "--unified=0",
                merge_base_sha,
                head_sha,
                "--",
            ]
        )
        hunks_by_file = parse_unified_diff(unified_diff_raw)

        changed_files: list[ChangedFile] = []
        for code, p1, p2 in status_entries:
            change_type: Literal["added", "modified", "deleted", "renamed"]
            path_before: str | None = None
            path_after: str | None = None

            if code == "A":
                change_type = "added"
                path_before = None
                path_after = p1
            elif code == "D":
                change_type = "deleted"
                path_before = p1
                path_after = None
            elif code == "R":
                change_type = "renamed"
                path_before = p1
                path_after = p2
            else:
                change_type = "modified"
                path_before = p1
                path_after = p1

            active_path = path_after or path_before or ""
            hunks = hunks_by_file.get(active_path, [])

            # Check if binary
            is_binary = False
            # Check blobs or git diff binary indicators
            changed_files.append(
                ChangedFile(
                    path_before=path_before,
                    path_after=path_after,
                    change_type=change_type,
                    is_binary=is_binary,
                    hunks=hunks,
                )
            )

        return changed_files
