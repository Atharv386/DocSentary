class GitError(RuntimeError):
    """Raised when a Git command fails."""

    def __init__(self, command: list[str], exit_code: int, stderr: str) -> None:
        self.command = command
        self.exit_code = exit_code
        self.stderr = stderr
        cmd_str = " ".join(command)
        super().__init__(f"Git command failed (exit {exit_code}): '{cmd_str}'\n{stderr}")
