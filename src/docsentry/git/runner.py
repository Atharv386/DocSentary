import subprocess
from pathlib import Path

from docsentry.git.errors import GitError


class GitRunner:
    """Safely executes Git CLI commands using subprocess with explicit argument lists."""

    def __init__(self, repo_root: Path, timeout_seconds: int = 30) -> None:
        self.repo_root = repo_root.resolve()
        self.timeout_seconds = timeout_seconds

    def run(self, args: list[str], check: bool = True) -> str:
        cmd = ["git", "-C", str(self.repo_root)] + args
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            if check and res.returncode != 0:
                raise GitError(cmd, res.returncode, res.stderr.strip())
            return res.stdout
        except subprocess.TimeoutExpired as exc:
            msg = f"Git command timed out after {self.timeout_seconds}s"
            raise GitError(cmd, 124, msg) from exc

    def run_bytes(self, args: list[str], check: bool = True) -> bytes:
        cmd = ["git", "-C", str(self.repo_root)] + args
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            if check and res.returncode != 0:
                stderr = res.stderr.decode("utf-8", errors="replace").strip()
                raise GitError(cmd, res.returncode, stderr)
            return res.stdout
        except subprocess.TimeoutExpired as exc:
            msg = f"Git command timed out after {self.timeout_seconds}s"
            raise GitError(cmd, 124, msg) from exc

    def validate_commit(self, ref: str) -> None:
        """Validate that ref points to an actual commit object."""
        self.run(["cat-file", "-e", f"{ref}^{{commit}}"])

    def resolve_sha(self, ref: str) -> str:
        """Resolve a branch or tag ref to a 40-character commit SHA."""
        out = self.run(["rev-parse", f"{ref}^{{commit}}"]).strip()
        return out

    def get_merge_base(self, base_sha: str, head_sha: str) -> str:
        """Compute the common ancestor between base and head."""
        return self.run(["merge-base", base_sha, head_sha]).strip()
