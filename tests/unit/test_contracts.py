from pathlib import Path

from docsentry.contracts import (
    ChangedFile,
    CodeFact,
    DiffHunk,
    DocSpan,
    EvidenceRef,
    Finding,
    ScanContext,
    ScanReport,
)


def test_scan_context_serialization() -> None:
    ctx = ScanContext(
        repo_root=Path("/tmp/repo"),
        base_sha="a" * 40,
        head_sha="b" * 40,
        merge_base_sha="c" * 40,
        scan_id="scan-001",
        config_hash="abc123",
        tool_version="0.1.0",
    )
    assert ctx.scan_id == "scan-001"
    dump = ctx.model_dump()
    assert dump["base_sha"] == "a" * 40


def test_code_fact_serialization() -> None:
    fact = CodeFact(
        fact_id="fact-1",
        language="python",
        path="src/client.py",
        qualified_name="client.connect",
        kind="default_changed",
        symbol="connect",
        member="timeout",
        before="30",
        after="60",
        line_before=12,
        line_after=12,
        source_change_id="change-1",
        static_confidence="high",
    )
    assert fact.kind == "default_changed"
    json_str = fact.model_dump_json()
    assert "default_changed" in json_str


def test_doc_span_serialization() -> None:
    span = DocSpan(
        span_id="span-1",
        path="docs/config.md",
        block_type="paragraph",
        heading_path=["Configuration", "Networking"],
        text="The default timeout is 30 seconds.",
        raw_text="The default timeout is 30 seconds.",
        line_start=23,
        line_end=23,
        inline_code=["timeout"],
    )
    assert span.line_start == 23
    assert span.inline_code == ["timeout"]


def test_scan_report_roundtrip() -> None:
    report = ScanReport(
        schema_version="1.0",
        scan_id="scan-2026-10-31-001",
        base_sha="abc123",
        head_sha="def456",
        merge_base_sha="abc123",
        tool_version="0.1.0",
        summary={"changed_files": 1, "findings": 1, "drift": 1},
        changed_files=[
            ChangedFile(
                path_before="src/client.py",
                path_after="src/client.py",
                change_type="modified",
                hunks=[
                    DiffHunk(
                        old_start=10,
                        old_count=5,
                        new_start=10,
                        new_count=5,
                        header="def connect():",
                        added_lines=["def connect(timeout=60):"],
                        removed_lines=["def connect(timeout=30):"],
                    )
                ],
            )
        ],
        findings=[
            Finding(
                finding_id="DG-0001",
                status="DRIFT",
                severity="high",
                rule_id="PY-DEFAULT-001",
                category="default_value_mismatch",
                title="Documented timeout default is outdated",
                explanation="The docs say 30; the updated function defaults to 60.",
                evidence=[
                    EvidenceRef(
                        evidence_id="E1",
                        role="code",
                        path="src/client.py",
                        line_start=12,
                        line_end=12,
                        quote="def connect(timeout=60):",
                        source_kind="ast_fact",
                    ),
                    EvidenceRef(
                        evidence_id="E2",
                        role="documentation",
                        path="docs/config.md",
                        line_start=23,
                        line_end=23,
                        quote="The default timeout is 30 seconds.",
                        source_kind="doc_span",
                    ),
                ],
                confidence=1.0,
                verification="deterministic",
            )
        ],
        warnings=[],
        duration_ms=450,
    )

    dumped = report.model_dump_json()
    loaded = ScanReport.model_validate_json(dumped)
    assert loaded.scan_id == "scan-2026-10-31-001"
    assert len(loaded.findings) == 1
    assert loaded.findings[0].severity == "high"
    assert loaded.findings[0].evidence[0].role == "code"
