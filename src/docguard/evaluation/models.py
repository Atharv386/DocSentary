from typing import Any, Literal

from pydantic import BaseModel, Field


class EvaluationCase(BaseModel):
    case_id: str
    category: Literal[
        "confirmed_drift",
        "negative_control",
        "ambiguous_edge_case",
        "doc_semantics",
    ]
    name: str
    description: str
    difficulty: Literal["low", "medium", "high", "adversarial"]
    target_engine: Literal["deterministic", "ai_assisted", "both"]
    files_base: dict[str, str]  # relative path -> content
    files_head: dict[str, str]  # relative path -> content
    expected_status: Literal["DRIFT", "POTENTIAL_DRIFT", "NO_DRIFT", "UNCERTAIN"]
    acceptable_statuses: list[str] = Field(default_factory=list)
    expected_rule_id: str | None = None
    expected_doc_file: str | None = None
    expected_doc_line_range: tuple[int, int] | None = None
    rationale: str


class EvaluationResult(BaseModel):
    case_id: str
    passed: bool
    expected_status: str
    actual_status: str
    actual_rule_id: str | None = None
    actual_findings_count: int = 0
    actual_doc_path: str | None = None
    actual_doc_lines: tuple[int, int] | None = None
    exact_location_match: bool = False
    evidence_valid: bool = False
    duration_ms: int = 0
    notes: str = ""


class ConfusionMatrix(BaseModel):
    true_positives: int = 0  # Expected DRIFT/POTENTIAL, Got DRIFT/POTENTIAL
    true_negatives: int = 0  # Expected NO_DRIFT/UNCERTAIN, Got NO_DRIFT/UNCERTAIN
    false_positives: int = 0  # Expected NO_DRIFT, Got DRIFT/POTENTIAL
    false_negatives: int = 0  # Expected DRIFT, Got NO_DRIFT


class EvaluationMetrics(BaseModel):
    total_cases: int
    passed_cases: int
    precision: float
    recall: float
    specificity: float
    f1_score: float
    exact_location_accuracy: float
    evidence_accuracy: float
    uncertain_rate: float
    average_latency_ms: float
    confusion_matrix: ConfusionMatrix
    category_breakdown: dict[str, dict[str, Any]]
