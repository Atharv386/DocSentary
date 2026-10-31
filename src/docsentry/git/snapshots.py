from pathlib import Path

from docsentry.git.errors import GitError
from docsentry.git.runner import GitRunner


class GitSnapshotService:
    """Retrieves file contents directly from Git commit snapshots."""

    def __init__(self, runner: GitRunner, max_file_bytes: int = 500000) -> None:
        self.runner = runner
        self.max_file_bytes = max_file_bytes

    def read_file(self, commit_sha: str, relative_path: str) -> str | None:
        """
        Reads a text file at a given commit SHA.
        Returns None if the file does not exist, is binary, or exceeds size limits.
        """
        # Validate path safety
        norm = Path(relative_path)
        if norm.is_absolute() or ".." in norm.parts:
            raise ValueError(f"Illegal path traversal attempt: {relative_path}")

        try:
            raw_bytes = self.runner.run_bytes(["show", f"{commit_sha}:{relative_path}"])
        except GitError:
            # File does not exist at this commit
            return None

        if len(raw_bytes) > self.max_file_bytes:
            return None

        # Check binary: check for NUL byte
        if b"\x00" in raw_bytes:
            return None

        try:
            return raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # Try utf-8 with fallback or return None
            return raw_bytes.decode("utf-8", errors="replace")
