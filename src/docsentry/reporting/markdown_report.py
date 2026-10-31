from pathlib import Path

from docsentry.contracts.findings import ScanReport


def render_markdown_report(report: ScanReport) -> str:
    lines: list[str] = []

    lines.append("# DocGuard Analysis Report")
    lines.append("")

    # Summary table
    drift = report.summary.get("drift", 0)
    potential = report.summary.get("potential_drift", 0)
    uncertain = report.summary.get("uncertain", 0)
    changed = report.summary.get("changed_files", 0)

    status_icon = "🔴" if drift > 0 else ("🟡" if potential > 0 else "🟢")
    summary_text = (
        f"**Status**: {status_icon} **{drift} Confirmed Drift** | "
        f"{potential} Potential | {uncertain} Uncertain"
    )
    lines.append(summary_text)
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("| :--- | :--- |")
    lines.append(f"| **Scan ID** | `{report.scan_id}` |")
    lines.append(f"| **Base Commit** | `{report.base_sha[:8]}` |")
    lines.append(f"| **Head Commit** | `{report.head_sha[:8]}` |")
    lines.append(f"| **Changed Files** | {changed} |")
    lines.append(f"| **Total Findings** | {len(report.findings)} |")
    lines.append(f"| **Duration** | {report.duration_ms} ms |")
    lines.append("")

    if not report.findings:
        lines.append("### ✓ No Documentation Drift Detected")
        lines.append(
            "All modified symbols, parameters, and defaults remain consistent with current docs."
        )
        lines.append("")
        return "\n".join(lines)

    lines.append("## Findings & Traceable Evidence")
    lines.append("")

    for idx, f in enumerate(report.findings, start=1):
        status_badge = f"`{f.status}`"
        sev_badge = f"**[{f.severity.upper()}]**"
        lines.append(f"### {idx}. {sev_badge} {status_badge} {f.title}")
        lines.append(f"- **Rule ID**: `{f.rule_id}` ({f.category})")
        lines.append(f"- **Verification**: `{f.verification}`")
        lines.append(f"- **Explanation**: {f.explanation}")
        if f.suggested_action:
            lines.append(f"- **Action**: *{f.suggested_action}*")
        lines.append("")

        # Evidence table / comparison
        code_ev = next((e for e in f.evidence if e.role == "code"), None)
        doc_ev = next((e for e in f.evidence if e.role == "documentation"), None)

        if code_ev and doc_ev:
            lines.append(
                "| Documentation (Outdated Statement) | Code Evidence (Actual Implementation) |"
            )
            lines.append("| :--- | :--- |")
            doc_loc = f"`{doc_ev.path}:{doc_ev.line_start}-{doc_ev.line_end}`"
            code_loc = f"`{code_ev.path}:{code_ev.line_start}`"
            row = (
                f'| **Location**: {doc_loc}<br><br>"{doc_ev.quote}" | '
                f"**Location**: {code_loc}<br><br>`{code_ev.quote}` |"
            )
            lines.append(row)
            lines.append("")
        elif f.evidence:
            for ev in f.evidence:
                ev_role = ev.role.capitalize()
                lines.append(f'- **{ev_role}** (`{ev.path}:{ev.line_start}`): "{ev.quote}"')
            lines.append("")

    if report.warnings:
        lines.append("## Scan Warnings & Observability")
        for w in report.warnings:
            lines.append(f"- ⚠️ {w}")
        lines.append("")

    return "\n".join(lines)


def write_markdown_report(report: ScanReport, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    content = render_markdown_report(report)
    output_file.write_text(content, encoding="utf-8")
