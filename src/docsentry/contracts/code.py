from typing import Any, Literal

from pydantic import BaseModel, Field


class CodeFact(BaseModel):
    fact_id: str
    language: Literal["python"] = "python"
    path: str
    qualified_name: str | None = None
    kind: Literal[
        "function_added",
        "function_removed",
        "function_renamed",
        "parameter_added",
        "parameter_removed",
        "parameter_renamed",
        "default_changed",
        "constant_changed",
        "config_flag_changed",
        "decorator_changed",
        "docstring_changed",
        "behavior_changed",
        "return_changed",
        "exception_changed",
        "parse_warning",
    ]
    category: Literal["syntactic", "behavioral"] = "syntactic"
    symbol: str | None = None
    member: str | None = None  # parameter, flag or constant
    before: str | None = None
    after: str | None = None
    line_before: int | None = None
    line_after: int | None = None
    source_change_id: str
    static_confidence: Literal["high", "medium", "low"]
    metadata: dict[str, Any] = Field(default_factory=dict)
