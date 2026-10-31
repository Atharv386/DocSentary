import re
from pathlib import Path

from docsentry.contracts.code import CodeFact
from docsentry.contracts.docs import DocSpan
from docsentry.contracts.findings import EvidenceRef, Finding

HISTORICAL_MARKERS = [
    "previously",
    "formerly",
    "before version",
    "prior to",
    "was ",
    "used to be",
    "upgrade from",
    "in version 1",
    "in v1",
]

HISTORICAL_DOC_NAMES = [
    "changelog.md",
    "history.md",
    "changes.md",
    "releases.md",
    "news.md",
    "migration.md",
]


def normalize_literal(val: str | None) -> str:
    if val is None:
        return ""
    val_str = str(val).strip().strip("'\"")
    return val_str


def is_historical_context(doc_span: DocSpan) -> bool:
    if getattr(doc_span, "claim_type", "") == "historical_migration":
        return True

    # 1. Check filename
    doc_file_name = Path(doc_span.path).name.lower()
    if doc_file_name in HISTORICAL_DOC_NAMES:
        return True

    # 2. Check headings for historical/release markers
    for h in doc_span.heading_path:
        hl = h.lower()
        if (
            re.search(r"\bv\d+\.\d+", hl)
            or "release" in hl
            or "migration" in hl
            or "changelog" in hl
        ):
            return True

    # 3. Check paragraph text markers
    span_lower = doc_span.text.lower()
    return any(marker in span_lower for marker in HISTORICAL_MARKERS)


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

    # Sibling symbol disambiguation:
    # If the span explicitly mentions an UNCHANGED sibling function from the same file,
    # but does NOT mention code_fact.symbol, do not attribute this span to code_fact!
    siblings = code_fact.metadata.get("sibling_symbols", [])
    if siblings and isinstance(siblings, list) and code_fact.symbol:
        has_symbol = (
            code_fact.symbol in doc_span.inline_code
            or re.search(rf"\b{re.escape(code_fact.symbol)}\b", span_text)
            or any(code_fact.symbol in h for h in doc_span.heading_path)
            or code_fact.symbol in doc_span.path
        )
        if not has_symbol:
            for sib in siblings:
                if (
                    sib in doc_span.inline_code
                    or re.search(rf"\b{re.escape(str(sib))}\b", span_text)
                    or any(str(sib) in h for h in doc_span.heading_path)
                    or str(sib) in doc_span.path
                ):
                    return None

    # Require member identifier mention in span
    mentions_member = bool(
        member in doc_span.inline_code
        or re.search(rf"\b{re.escape(member)}\b", span_text, re.IGNORECASE)
    )

    # Require exact literal match with word/token boundaries
    mentions_old = bool(re.search(rf"\b{re.escape(old_val)}\b", span_text))
    mentions_new = bool(new_val and re.search(rf"\b{re.escape(new_val)}\b", span_text))

    if not (mentions_member and mentions_old):
        return None

    # If the docs already mention the new value or discuss historical versions, no drift
    if mentions_new or is_historical_context(doc_span):
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
