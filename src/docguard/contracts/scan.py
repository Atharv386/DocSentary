from pathlib import Path

from pydantic import BaseModel, Field


class ScanContext(BaseModel):
    repo_root: Path
    base_sha: str
    head_sha: str
    merge_base_sha: str
    scan_id: str
    source_globs: list[str] = Field(default_factory=lambda: ["**/*.py"])
    docs_globs: list[str] = Field(default_factory=lambda: ["**/*.md", "**/*.mdx"])
    exclude_globs: list[str] = Field(
        default_factory=lambda: [
            "**/.venv/**",
            "**/site-packages/**",
            "**/build/**",
            "**/dist/**",
            "**/generated/**",
            "**/vendor/**",
        ]
    )
    model_enabled: bool = True
    config_hash: str
    tool_version: str
