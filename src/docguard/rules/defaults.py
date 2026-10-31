import re

from docguard.contracts.code import CodeFact
from docguard.contracts.docs import DocSpan
from docguard.contracts.findings import EvidenceRef, Finding

HISTORICAL_MARKERS = [
    "previously",
    "formerly",
    "before version",
    "prior to",
    "was ",
    "used to be",
]


def normalize_literal(val: str | None) -> str:
    if val is None:
        return ""
    val_str = str(val).strip().strip("'\"")
    return val_str


def detect_default_drift(
    code_fact: CodeFact,
    doc_span: DocSpan,
    finding_id: str,
) -> Finding | None:
    """
    PY-DEFAULT-001: Stale default value mismatch.
    Triggers when code changed default value, but docs still reference the old default.
    """
    if code_fact.kind != "default_changed":
        return None

    old_val = normalize_literal(code_fact.before)
    new_val = normalize_literal(code_fact.after)
    member = code_fact.member or code_fact.symbol or ""

    span_text = doc_span.text
    span_lower = span_text.lower()

    # Require member identifier mention in span
    mentions_member = bool(
        member in doc_span.inline_code
        or re.search(rf"\b{re.escape(member)}\b", span_text, re.IGNORECASE)
    )

    # Require exact literal match with word/token boundaries
    mentions_old = bool(re.search(rf"\b{re.escape(old_val)}\b", span_text))
    mentions_new = bool(new_val and re.search(rf"\b{re.escape(new_val)}\b", span_text))

    # Check for historical explanation context
    has_historical = any(marker in span_lower for marker in HISTORICAL_MARKERS)

    if not (mentions_member and mentions_old):
        return None

    # If the docs already mention the new value or discuss historical versions, no drift
    if mentions_new or has_historical:
        return None

    # Construct evidence
    code_quote = f"def {code_fact.symbol}(..., {member}={code_fact.after}): ..."
    doc_quote = doc_span.raw_text

    return Finding(
        finding_id=finding_id,
        status="DRIFT",
        severity="high",
        rule_id="PY-DEFAULT-001",
        category="default_value_mismatch",
        title=f"Documented default for '{member}' is outdated",
        explanation=(
            f"The documentation states the default is {old_val}, but the updated code "
            f"in {code_fact.path} defaults {member} to {new_val}."
        ),
        evidence=[
            EvidenceRef(
                evidence_id="E1",
                role="code",
                path=code_fact.path,
                line_start=code_fact.line_after or 1,
                line_end=code_fact.line_after or 1,
                quote=code_quote,
                source_kind="ast_fact",
            ),
            EvidenceRef(
                evidence_id="E2",
                role="documentation",
                path=doc_span.path,
                line_start=doc_span.line_start,
                line_end=doc_span.line_end,
                quote=doc_quote,
                source_kind="doc_span",
            ),
        ],
        confidence=1.0,
        verification="deterministic",
        suggested_action=(
            f"Update '{doc_span.path}:{doc_span.line_start}' to reflect default {member}={new_val}."
        ),
    )
