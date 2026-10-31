import hashlib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ScopeConfig(BaseModel):
    source_globs: list[str] = Field(default_factory=lambda: ["**/*.py"])
    docs_globs: list[str] = Field(default_factory=lambda: ["**/*.md", "**/*.mdx"])
    exclude_globs: list[str] = Field(
        default_factory=lambda: [
            "**/.venv/**",
            "**/site-packages/**",
            "**/build/**",
            "**/dist/**",
            "**/vendor/**",
        ]
    )


class LimitsConfig(BaseModel):
    max_files: int = 250
    max_file_bytes: int = 500000
    max_doc_spans_per_fact: int = 5
    max_model_context_chars: int = 18000


class ModelConfig(BaseModel):
    enabled: bool = True
    timeout_seconds: int = 30
    max_retries: int = 1


class ReportConfig(BaseModel):
    include_no_drift: bool = False
    include_uncertain: bool = True
    fail_on: str = "never"


class DocGuardConfig(BaseModel):
    version: int = 1
    scope: ScopeConfig = Field(default_factory=ScopeConfig)
    limits: LimitsConfig = Field(default_factory=LimitsConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)

    def compute_hash(self) -> str:
        data = self.model_dump_json()
        return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


def load_config(config_path: Path | None = None) -> tuple[DocGuardConfig, str]:
    """Loads configuration from YAML file or returns defaults."""
    if config_path and config_path.is_file():
        raw_text = config_path.read_text(encoding="utf-8")
        try:
            # Safe YAML parsing using simple parser or standard yaml if present
            # We will use PyYAML or lightweight loader
            import yaml  # type: ignore

            data: dict[str, Any] = yaml.safe_load(raw_text) or {}
            cfg = DocGuardConfig.model_validate(data)
            return cfg, cfg.compute_hash()
        except ImportError:
            # Fallback if pyyaml is not installed

            # If plain defaults
            cfg = DocGuardConfig()
            return cfg, cfg.compute_hash()
    cfg = DocGuardConfig()
    return cfg, cfg.compute_hash()
