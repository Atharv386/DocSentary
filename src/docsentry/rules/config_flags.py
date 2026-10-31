import re

from docsentry.contracts.code import CodeFact
from docsentry.contracts.docs import DocSpan
from docsentry.contracts.findings import EvidenceRef, Finding


def detect_config_flag_drift(
    code_fact: CodeFact,
    doc_span: DocSpan,
    finding_id: str,
) -> Finding | None:
    """
    PY-CONFIG-004: Stale CLI flag or configuration key.
    Triggers when a CLI flag or config key changes/removes, but documentation still references it.
    """
    if code_fact.kind != "config_flag_changed":
        return None

    flag = code_fact.member or ""
    if not flag:
        return None

    span_text = doc_span.text

    mentions_flag = bool(
        flag in doc_span.inline_code
        or re.search(rf"(?:^|\s|`){re.escape(flag)}(?:$|\s|`|=)", span_text)
    )

    if not mentions_flag:
        return None

    code_quote = f"CLI flag '{flag}' was modified or removed in {code_fact.path}"

    return Finding(
        finding_id=finding_id,
        status="DRIFT",
        severity="high",
        rule_id="PY-CONFIG-004",
        category="stale_config_flag",
        title=f"Documentation references obsolete flag '{flag}'",
        explanation=(
            f"CLI flag '{flag}' was modified or removed in {code_fact.path}, "
            f"but documentation still documents it."
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
        confidence=0.98,
        verification="deterministic",
        suggested_action=(
            f"Update reference to '{flag}' in '{doc_span.path}:{doc_span.line_start}'."
        ),
    )
