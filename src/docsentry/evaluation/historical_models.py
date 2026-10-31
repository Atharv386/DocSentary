from typing import Any, Literal

from pydantic import BaseModel, Field


class HistoricalCase(BaseModel):
    case_id: str
    repository: str  # e.g. "encode/httpx", "pallets/click"
    language: Literal["python", "typescript", "javascript"]
    split: Literal["dev", "val", "test"]  # Repository-level split
    code_commit: str  # Actual historical code commit SHA
    documentation_fix_commit: str | None = None  # Actual later doc fix SHA (if drift)
    evaluation_base_commit: str  # Parent SHA before code change
    evaluation_head_commit: str  # Code commit SHA (intermediate state where docs are stale)
    drift_type: Literal[
        "default_value_change",
        "parameter_removed",
        "parameter_renamed",
        "symbol_removed",
        "constant_value_change",
        "config_flag_change",
        "behavioral_contract",
        "return_type_contract",
        "exception_contract",
        "concurrency_contract",
        "negative_control_refactor",
        "negative_control_private_rename",
        "negative_control_test_only",
        "negative_control_doc_in_sync",
        "negative_control_historical_doc",
    ]
    documentation_file: str
    incorrect_sentence: str | None = None  # None for negative controls
    expected_code_reference: str
    expected_finding: bool  # True for real drift, False for negative control
    expected_rule_id: str | None = None
    files_base: dict[str, str]  # Exact historical file content at base
    files_head: dict[str, str]  # Exact historical file content at head
    ground_truth_source: str  # Actual PR, issue, or commit URL
    ground_truth_explanation: str
    review_status: Literal["independently_verified", "unverified"] = "independently_verified"


class HistoricalReplayResult(BaseModel):
    case_id: str
    repository: str
    split: str
    configuration: Literal["deterministic", "qwen3_8b_only", "selective_hybrid"]
    passed: bool
    expected_finding: bool
    actual_drift_detected: bool
    actual_status: str
    actual_rule_id: str | None = None
    actual_findings_count: int = 0
    actual_doc_path: str | None = None
    actual_doc_lines: tuple[int, int] | None = None
    exact_location_match: bool = False
    correct_code_attribution: bool = False
    evidence_valid: bool = False
    abstention_triggered: bool = False
    model_invocations: int = 0
    raw_model_status: str | None = None
    duration_ms: int = 0
    notes: str = ""


class HistoricalConfusionMatrix(BaseModel):
    true_positives: int = 0
    true_negatives: int = 0
    false_positives: int = 0
    false_negatives: int = 0


class HistoricalMetrics(BaseModel):
    configuration: str
    total_cases: int
    passed_cases: int
    precision: float | None = None  # None if TP + FP == 0
    recall: float | None = None  # None if TP + FN == 0
    specificity: float | None = None  # None if TN + FP == 0
    f1_score: float | None = None
    exact_location_accuracy: float = 0.0
    code_attribution_accuracy: float = 0.0
    evidence_accuracy: float = 0.0
    average_latency_ms: float = 0.0
    total_model_invocations: int = 0
    confusion_matrix: HistoricalConfusionMatrix = Field(default_factory=HistoricalConfusionMatrix)
    per_repository_stats: dict[str, dict[str, Any]] = Field(default_factory=dict)
    per_category_stats: dict[str, dict[str, Any]] = Field(default_factory=dict)
