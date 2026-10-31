import re

from docguard.contracts.code import CodeFact
from docguard.contracts.docs import DocSpan
from docguard.contracts.findings import EvidenceRef, Finding


def detect_signature_drift(
    code_fact: CodeFact,
    doc_span: DocSpan,
    finding_id: str,
) -> Finding | None:
    """
    PY-PARAM-002: Stale parameter mention.
    Triggers when a parameter is removed or renamed, but docs still reference it.
    """
    if code_fact.kind != "parameter_removed":
        return None

    removed_param = code_fact.member or ""
    if not removed_param:
        return None

    span_text = doc_span.text

    # Check if doc mentions the removed parameter
    mentions_removed = bool(
        removed_param in doc_span.inline_code
        or re.search(rf"\b{re.escape(removed_param)}\b", span_text)
    )

    if not mentions_removed:
        return None

    is_exact_code_or_sig = doc_span.block_type in ("fence", "table_cell") or (
        removed_param in doc_span.inline_code
    )
    status = "DRIFT" if is_exact_code_or_sig else "POTENTIAL_DRIFT"

    symbol_name = code_fact.symbol or "function"
    code_quote = f"Parameter '{removed_param}' was removed from {symbol_name}()"

    return Finding(
        finding_id=finding_id,
        status=status,
        severity="high" if status == "DRIFT" else "medium",
        rule_id="PY-PARAM-002",
        category="stale_parameter",
        title=f"Documentation references removed parameter '{removed_param}'",
        explanation=(
            f"Parameter '{removed_param}' was removed from {symbol_name} in {code_fact.path}, "
            f"but documentation still refers to it."
        ),
        evidence=[
            EvidenceRef(
                evidence_id="E1",
                role="code",
                path=code_fact.path,
                line_start=code_fact.line_after or code_fact.line_before or 1,
                line_end=code_fact.line_after or code_fact.line_before or 1,
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
        confidence=0.95 if status == "DRIFT" else 0.80,
        verification="deterministic",
        suggested_action=(
            f"Remove reference to '{removed_param}' in '{doc_span.path}:{doc_span.line_start}'."
        ),
    )
