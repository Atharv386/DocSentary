from unittest.mock import MagicMock

from docsentry.contracts.findings import EvidenceRef, Finding
from docsentry.git.snapshots import GitSnapshotService
from docsentry.validation.evidence import EvidenceValidator


def _make_finding(
    status: str = "DRIFT",
    severity: str = "high",
    code_path: str | None = "src/api.py",
    doc_path: str | None = "docs/api.md",
    doc_quote: str = "Default timeout is 30 seconds.",
    finding_id: str = "f-1",
) -> Finding:
    evidence = []
    if code_path:
        evidence.append(
            EvidenceRef(
                evidence_id="ev-code-1",
                role="code",
                path=code_path,
                line_start=10,
                line_end=12,
                quote="def __init__(self, timeout: int = 60):",
                source_kind="ast_fact",
            )
        )
    if doc_path:
        evidence.append(
            EvidenceRef(
                evidence_id="ev-doc-1",
                role="documentation",
                path=doc_path,
                line_start=5,
                line_end=5,
                quote=doc_quote,
                source_kind="doc_span",
            )
        )
    return Finding(
        finding_id=finding_id,
        rule_id="RULE-TEST",
        category="api_signature",
        title="Test Drift Finding",
        status=status,
        severity=severity,
        explanation="Testing validation.",
        evidence=evidence,
        verification="deterministic",
    )


def test_adversarial_valid_evidence_passes():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = (
        "# API Guide\nDefault timeout is 30 seconds for all network requests."
    )

    validator = EvidenceValidator(mock_service)
    finding = _make_finding()
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert len(result) == 1
    assert result[0].status == "DRIFT"
    assert result[0].severity == "high"


def test_adversarial_fabricated_doc_path():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = None  # file does not exist in commit

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(doc_path="nonexistent/fake_docs.md")
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert len(result) == 1
    assert result[0].status == "UNCERTAIN"
    assert result[0].severity == "info"
    assert "downgraded to UNCERTAIN" in result[0].explanation


def test_adversarial_fabricated_doc_quote():
    mock_service = MagicMock(spec=GitSnapshotService)
    # File exists, but does not contain the claimed quote
    mock_service.read_file.return_value = "# API Guide\nAll requests use exponential backoff."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(doc_quote="Completely fabricated hallucination about timeout.")
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert len(result) == 1
    assert result[0].status == "UNCERTAIN"
    assert result[0].severity == "info"
    assert "downgraded to UNCERTAIN" in result[0].explanation


def test_adversarial_missing_code_evidence():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Default timeout is 30 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(code_path=None)  # No code evidence
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert len(result) == 1
    assert result[0].status == "UNCERTAIN"
    assert result[0].severity == "info"


def test_adversarial_missing_doc_evidence():
    mock_service = MagicMock(spec=GitSnapshotService)

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(doc_path=None)  # No doc evidence
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert len(result) == 1
    assert result[0].status == "UNCERTAIN"
    assert result[0].severity == "info"


def test_adversarial_non_drift_status_preserved():
    mock_service = MagicMock(spec=GitSnapshotService)

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(status="NO_DRIFT", severity="info")
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert len(result) == 1
    assert result[0].status == "NO_DRIFT"
    mock_service.read_file.assert_not_called()


def test_adversarial_severity_sorting():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Default timeout is 30 seconds."

    validator = EvidenceValidator(mock_service)
    f_low = _make_finding(severity="low", finding_id="f-low")
    f_crit = _make_finding(severity="critical", finding_id="f-crit")
    f_med = _make_finding(severity="medium", finding_id="f-med")

    result = validator.validate_findings([f_low, f_crit, f_med], head_sha="abc12345")

    assert [f.finding_id for f in result] == ["f-crit", "f-med", "f-low"]
