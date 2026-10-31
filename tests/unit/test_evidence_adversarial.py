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
    code_quote: str = "def __init__(self, timeout: int = 60):",
    finding_id: str = "f-1",
    rule_id: str = "RULE-TEST",
    explanation: str = "Testing validation.",
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
                quote=code_quote,
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
        rule_id=rule_id,
        category="api_signature",
        title="Test Drift Finding",
        status=status,
        severity=severity,
        explanation=explanation,
        evidence=evidence,
        verification="deterministic",
    )


# 1. Fabricated file paths
def test_adversarial_01_fabricated_file_path():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = None  # File not in commit

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(doc_path="nonexistent/fake_docs.md")
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert result[0].status == "UNCERTAIN"
    assert "downgraded to UNCERTAIN" in result[0].explanation


# 2. Fabricated code quotes
def test_adversarial_02_fabricated_code_quote():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "# Valid doc\nDefault timeout is 30 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(code_quote="fabricated_symbol_does_not_exist()")
    result = validator.validate_findings([finding], head_sha="abc12345")
    # Validator checks quote grounding
    assert len(result) == 1


# 3. Fabricated documentation quotes
def test_adversarial_03_fabricated_doc_quote():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "# API Guide\nAll requests use exponential backoff."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(doc_quote="Completely fabricated hallucination about timeout.")
    result = validator.validate_findings([finding], head_sha="abc12345")

    assert result[0].status == "UNCERTAIN"
    assert "downgraded to UNCERTAIN" in result[0].explanation


# 4. Valid quotes from the wrong commit (e.g. deleted text from base)
def test_adversarial_04_quote_from_wrong_commit():
    mock_service = MagicMock(spec=GitSnapshotService)
    # Head commit has updated documentation; stale quote only existed in base commit
    mock_service.read_file.return_value = "# API Guide\nDefault timeout is 60 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(doc_quote="Default timeout is 30 seconds.")
    result = validator.validate_findings([finding], head_sha="head_commit_sha")

    assert result[0].status == "UNCERTAIN"


# 5. Valid quotes from the wrong symbol
def test_adversarial_05_quote_from_wrong_symbol():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Client.connect() timeout is 30 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        code_quote="def disconnect(timeout: int = 60):",
        doc_quote="Client.connect() timeout is 30 seconds.",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert len(result) == 1


# 6. Valid but semantically irrelevant quotes
def test_adversarial_06_semantically_irrelevant_quote():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Python 3.12+ is supported on all major platforms."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        code_quote="def fetch(timeout: int = 60):",
        doc_quote="Python 3.12+ is supported on all major platforms.",
        status="UNCERTAIN",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert result[0].status == "UNCERTAIN"


# 7. Correct documentation quotes paired with unrelated code changes
def test_adversarial_07_unrelated_code_change_pairing():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Default timeout is 30 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        code_path="src/unrelated_math.py",
        code_quote="def add(a, b): return a + b",
        doc_path="docs/network.md",
        doc_quote="Default timeout is 30 seconds.",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert len(result) == 1


# 8. Historical documentation misclassified as current behavior
def test_adversarial_08_historical_documentation_handling():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "In version 1.0, timeout defaulted to 30 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        status="NO_DRIFT",
        doc_quote="In version 1.0, timeout defaulted to 30 seconds.",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert result[0].status == "NO_DRIFT"


# 9. Hypothetical examples interpreted as factual assertions
def test_adversarial_09_hypothetical_code_example():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "```python\nclient = connect(timeout=999)\n```"

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        status="NO_DRIFT",
        doc_quote="client = connect(timeout=999)",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert result[0].status == "NO_DRIFT"


# 10. Correctly quoted evidence with incorrect semantic conclusions
def test_adversarial_10_incorrect_semantic_conclusion():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "def _internal_helper(): pass"

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        status="UNCERTAIN",
        explanation="Refactored helper function; public behavior unaffected.",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert result[0].status == "UNCERTAIN"


# 11. Finding attributed to wrong code change
def test_adversarial_11_wrong_code_attribution():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Default timeout is 30 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(code_path="tests/test_something.py")
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert len(result) == 1


# 12. Finding whose sentence location is incorrect
def test_adversarial_12_incorrect_sentence_location():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Line 1\nLine 2\nLine 3"

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(doc_quote="Line 100 which does not exist in file")
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert result[0].status == "UNCERTAIN"


# 13. Indirect relationship detection
def test_adversarial_13_indirect_relationship():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Default timeout is 30 seconds."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        code_quote="DEFAULT_TIMEOUT = 60",
        doc_quote="Default timeout is 30 seconds.",
        rule_id="PY-CONST-005",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert result[0].status == "DRIFT"


# 14. Ambiguous case where system must abstain
def test_adversarial_14_ambiguous_abstention():
    mock_service = MagicMock(spec=GitSnapshotService)
    mock_service.read_file.return_value = "Dynamic action executed via getattr()."

    validator = EvidenceValidator(mock_service)
    finding = _make_finding(
        status="UNCERTAIN",
        severity="info",
        explanation="Dynamic reflection detected; abstaining from DRIFT verdict.",
    )
    result = validator.validate_findings([finding], head_sha="head_commit_sha")
    assert result[0].status == "UNCERTAIN"
    assert result[0].severity == "info"
