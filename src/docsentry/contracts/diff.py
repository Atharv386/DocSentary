from typing import Literal

from pydantic import BaseModel, Field


class DiffHunk(BaseModel):
    old_start: int | None
    old_count: int | None
    new_start: int | None
    new_count: int | None
    header: str | None = None
    added_lines: list[str] = Field(default_factory=list)
    removed_lines: list[str] = Field(default_factory=list)


class ChangedFile(BaseModel):
    path_before: str | None
    path_after: str | None
    change_type: Literal["added", "modified", "deleted", "renamed"]
    is_binary: bool = False
    hunks: list[DiffHunk] = Field(default_factory=list)
    old_blob_sha: str | None = None
    new_blob_sha: str | None = None
