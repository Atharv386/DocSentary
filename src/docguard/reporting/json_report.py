import json
from pathlib import Path

from docguard.contracts.findings import ScanReport


def write_json_report(report: ScanReport, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(report.model_dump(), f, indent=2)
