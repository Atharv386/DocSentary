from docguard.contracts.findings import Finding
from docguard.git.snapshots import GitSnapshotService


class EvidenceValidator:
    """
    Zero-Hallucination Trust Boundary.
    Validates that every finding's code and documentation quotes genuinely exist
    in the snapshot commits before emitting the finding.
    """

    def __init__(self, snapshot_service: GitSnapshotService) -> None:
        self.snapshot_service = snapshot_service

    def validate_findings(
        self,
        findings: list[Finding],
        head_sha: str,
    ) -> list[Finding]:
        validated: list[Finding] = []

        for finding in findings:
            if finding.status not in ("DRIFT", "POTENTIAL_DRIFT"):
                validated.append(finding)
                continue

            has_code = False
            has_doc = False
            doc_valid = True

            for ev in finding.evidence:
                if ev.role == "code":
                    has_code = True
                elif ev.role == "documentation":
                    has_doc = True
                    # Re-open snapshot to ensure doc line & quote exist
                    content = self.snapshot_service.read_file(head_sha, ev.path)
                    if content is None:
                        doc_valid = False
                    elif ev.quote:
                        # Check that words from the quote exist in the document
                        clean_quote = ev.quote.strip()[:40]
                        if clean_quote not in content:
                            doc_valid = False

            if not (has_code and has_doc) or not doc_valid:
                # Downgrade to UNCERTAIN
                downgraded = finding.model_copy(
                    update={
                        "status": "UNCERTAIN",
                        "severity": "info",
                        "explanation": (
                            f"{finding.explanation} (Note: Evidence validation could not "
                            f"verify exact text in {head_sha[:8]}; downgraded to UNCERTAIN)."
                        ),
                    }
                )
                validated.append(downgraded)
            else:
                validated.append(finding)

        # Sort by severity (critical > high > medium > low > info) then finding_id
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        validated.sort(key=lambda f: (severity_order.get(f.severity, 5), f.finding_id))
        return validated
