from typing import Sequence

from docguard.ai.client import ModelClient
from docguard.ai.protocol import EvidenceBundle, EvidenceItem
from docguard.contracts.code import CodeFact
from docguard.contracts.docs import CandidateLink, DocSpan
from docguard.contracts.findings import EvidenceRef, Finding


class SemanticModelVerifier:
    """Bounded AI-assisted verifier for behavioral documentation drift."""

    def __init__(self, client: ModelClient | None = None) -> None:
        self.client = client or ModelClient()

    def verify_candidates(
        self,
        facts: Sequence[CodeFact],
        spans: Sequence[DocSpan],
        candidates: Sequence[CandidateLink],
        covered_doc_spans: set[tuple[str, int]],
    ) -> list[Finding]:
        fact_map = {f.fact_id: f for f in facts}
        span_map = {s.span_id: s for s in spans}

        semantic_findings: list[Finding] = []

        # Find candidates not covered by deterministic rules
        for link in candidates:
            if link.score < 0.4:
                continue

            fact = fact_map.get(link.code_fact_id)
            span = span_map.get(link.doc_span_id)
            if not fact or not span:
                continue

            # Skip spans already diagnosed by deterministic rules
            if (span.path, span.line_start) in covered_doc_spans:
                continue

            # Only verify behavioral or signature changes not already flagged
            rule_id = "PY-BEHAVIOR-006"

            # Construct bounded evidence items
            code_summary = (
                f"{fact.kind}: {fact.member or fact.symbol} "
                f"(before={fact.before}, after={fact.after})"
            )
            code_ev = EvidenceItem(
                evidence_id="CODE-1",
                role="code",
                path=fact.path,
                line_start=fact.line_after or fact.line_before or 1,
                line_end=fact.line_after or fact.line_before or 1,
                quote=code_summary,
                source_kind="ast_fact",
            )
            doc_ev = EvidenceItem(
                evidence_id="DOC-1",
                role="documentation",
                path=span.path,
                line_start=span.line_start,
                line_end=span.line_end,
                quote=span.raw_text,
                source_kind="doc_span",
            )

            bundle = EvidenceBundle(
                bundle_id=f"bundle-{fact.fact_id}-{span.span_id}",
                code_fact_id=fact.fact_id,
                code_fact_summary=f"{fact.kind} on {fact.symbol or fact.path}",
                code_path=fact.path,
                code_before=fact.before,
                code_after=fact.after,
                evidence_items=[code_ev, doc_ev],
            )

            assessment = self.client.verify_bundle(bundle)

            if assessment.status in ("DRIFT", "POTENTIAL_DRIFT", "UNCERTAIN"):
                finding_id = f"DG-AI-{len(semantic_findings) + 1:03d}"
                f_evidence = [
                    EvidenceRef(
                        evidence_id="E1",
                        role="code",
                        path=code_ev.path,
                        line_start=code_ev.line_start,
                        line_end=code_ev.line_end,
                        quote=code_ev.quote,
                        source_kind="ast_fact",
                    ),
                    EvidenceRef(
                        evidence_id="E2",
                        role="documentation",
                        path=doc_ev.path,
                        line_start=doc_ev.line_start,
                        line_end=doc_ev.line_end,
                        quote=doc_ev.quote,
                        source_kind="doc_span",
                    ),
                ]

                target_name = fact.symbol or fact.path
                semantic_findings.append(
                    Finding(
                        finding_id=finding_id,
                        status=assessment.status,
                        severity=assessment.severity,
                        rule_id=rule_id,
                        category="behavioral_drift",
                        title=f"Behavioral change in '{target_name}' may affect documentation",
                        explanation=assessment.explanation,
                        evidence=f_evidence,
                        confidence=0.75 if assessment.status == "POTENTIAL_DRIFT" else None,
                        verification="model_assisted",
                        suggested_action=assessment.suggested_action,
                    )
                )

        return semantic_findings
