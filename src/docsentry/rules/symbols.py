import re

from docsentry.contracts.code import CodeFact
from docsentry.contracts.docs import DocSpan
from docsentry.contracts.findings import EvidenceRef, Finding


def detect_symbol_drift(
    code_fact: CodeFact,
    doc_span: DocSpan,
    finding_id: str,
) -> Finding | None:
    """
    PY-SYMBOL-003: Removed symbol reference.
    Triggers when a function/class is removed, but documentation still references it.
    """
    if code_fact.kind != "function_removed":
        return None

    symbol = code_fact.symbol or ""
    if not symbol:
        return None

    span_text = doc_span.text

    mentions_symbol = bool(
        symbol in doc_span.inline_code or re.search(rf"\b{re.escape(symbol)}\b", span_text)
    )

    if not mentions_symbol:
        return None

    code_quote = f"def {symbol}(...): removed from {code_fact.path}"

    return Finding(
        finding_id=finding_id,
        status="POTENTIAL_DRIFT",
        severity="medium",
        rule_id="PY-SYMBOL-003",
        category="removed_symbol",
        title=f"Documentation references removed symbol '{symbol}'",
        explanation=(
            f"Function '{symbol}' was removed in {code_fact.path}, "
            f"but documentation still refers to it."
        ),
        evidence=[
            EvidenceRef(
                evidence_id="E1",
                role="code",
                path=code_fact.path,
                line_start=code_fact.line_before or 1,
                line_end=code_fact.line_before or 1,
                quote=code_quote,
                source_kind="ast_fact",
            ),
            EvidenceRef(
                evidence_id="E2",
                role="documentation",
                path=doc_span.path,
                line_start=doc_span.line_start,
                line_end=doc_span.line_end,
                quote=doc_span.raw_text,
                source_kind="doc_span",
            ),
        ],
        confidence=0.85,
        verification="deterministic",
        suggested_action=(
            f"Update '{doc_span.path}:{doc_span.line_start}' to replace obsolete '{symbol}()'."
        ),
    )
