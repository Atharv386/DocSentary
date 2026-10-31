import re

from docguard.contracts.code import CodeFact
from docguard.contracts.docs import DocSpan
from docguard.contracts.findings import EvidenceRef, Finding


def detect_constant_drift(
    code_fact: CodeFact,
    doc_span: DocSpan,
    finding_id: str,
) -> Finding | None:
    """
    PY-CONST-005: Stale constant value mismatch.
    Triggers when a constant changes value, but docs still reference the old constant value.
    """
    if code_fact.kind != "constant_changed":
        return None

    constant_name = code_fact.member or code_fact.symbol or ""
    old_val = str(code_fact.before).strip().strip("'\"") if code_fact.before else ""
    new_val = str(code_fact.after).strip().strip("'\"") if code_fact.after else ""

    span_text = doc_span.text

    # Check if doc mentions constant_name OR any parameter linked to this constant
    linked_params = code_fact.metadata.get("linked_params", [])
    if not isinstance(linked_params, list):
        linked_params = []

    mentions_name = bool(
        constant_name in doc_span.inline_code
        or re.search(rf"\b{re.escape(constant_name)}\b", span_text)
        or any(
            p in doc_span.inline_code or re.search(rf"\b{re.escape(str(p))}\b", span_text)
            for p in linked_params
        )
    )

    mentions_old = bool(old_val and re.search(rf"\b{re.escape(old_val)}\b", span_text))
    mentions_new = bool(new_val and re.search(rf"\b{re.escape(new_val)}\b", span_text))

    if not (mentions_name and mentions_old) or mentions_new:
        return None

    code_quote = f"{constant_name} = {code_fact.after}  # previously {code_fact.before}"

    return Finding(
        finding_id=finding_id,
        status="DRIFT",
        severity="high",
        rule_id="PY-CONST-005",
        category="constant_value_mismatch",
        title=f"Documented constant '{constant_name}' is outdated",
        explanation=(
            f"Constant '{constant_name}' was updated from {old_val} to {new_val} in "
            f"{code_fact.path}, but documentation still states {old_val}."
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
                quote=doc_span.raw_text,
                source_kind="doc_span",
            ),
        ],
        confidence=1.0,
        verification="deterministic",
        suggested_action=(
            f"Update '{doc_span.path}:{doc_span.line_start}' to reflect {constant_name}={new_val}."
        ),
    )
