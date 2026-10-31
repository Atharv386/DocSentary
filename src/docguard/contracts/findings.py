from typing import Literal

from pydantic import BaseModel, Field

from docguard.contracts.diff import ChangedFile


class EvidenceRef(BaseModel):
    evidence_id: str
    role: Literal["code", "documentation"]
    path: str
    line_start: int
    line_end: int
    quote: str
    source_kind: Literal["ast_fact", "diff_hunk", "doc_span"]


class Finding(BaseModel):
    finding_id: str
    status: Literal["DRIFT", "POTENTIAL_DRIFT", "NO_DRIFT", "UNCERTAIN"]
    severity: Literal["critical", "high", "medium", "low", "info"]
    rule_id: str
    category: str
    title: str
    explanation: str
    evidence: list[EvidenceRef] = Field(default_factory=list)
    confidence: float | None = None  # model estimate, not calibrated probability
    verification: Literal["deterministic", "model_assisted", "human_fixture"]
    suggested_action: str | None = None


class ScanReport(BaseModel):
    schema_version: str = "1.0"
    scan_id: str
    base_sha: str
    head_sha: str
    merge_base_sha: str
    tool_version: str
    model_id: str | None = None
    summary: dict[str, int | float | str]
    changed_files: list[ChangedFile]
    findings: list[Finding] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    duration_ms: int
