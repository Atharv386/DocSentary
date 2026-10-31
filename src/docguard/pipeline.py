import fnmatch
import time
from pathlib import Path
from typing import NamedTuple

from docguard.ai.verifier import SemanticModelVerifier
from docguard.contracts.code import CodeFact
from docguard.contracts.diff import ChangedFile
from docguard.contracts.docs import DocSpan
from docguard.contracts.findings import ScanReport
from docguard.contracts.scan import ScanContext
from docguard.extractors.markdown import MarkdownExtractor
from docguard.extractors.python_ast import compare_python_facts
from docguard.git.diff import GitDiffService
from docguard.git.snapshots import GitSnapshotService
from docguard.mapping.candidates import CandidateMapper
from docguard.rules.engine import DeterministicRuleEngine
from docguard.validation.evidence import EvidenceValidator


class Dependencies(NamedTuple):
    git_diff_service: GitDiffService
    git_snapshot_service: GitSnapshotService
    markdown_extractor: MarkdownExtractor
    candidate_mapper: CandidateMapper
    rule_engine: DeterministicRuleEngine
    model_verifier: SemanticModelVerifier
    evidence_validator: EvidenceValidator


def path_matches_globs(path: str, globs: list[str]) -> bool:
    clean_p = path.replace("\\", "/")
    return any(fnmatch.fnmatch(clean_p, g) or fnmatch.fnmatch(Path(clean_p).name, g) for g in globs)


def scan_repository(context: ScanContext, deps: Dependencies) -> ScanReport:
    """
    Executes the end-to-end DocGuard analysis pipeline.
    """
    start_time = time.perf_counter()
    warnings: list[str] = []

    # 1. Resolve diff between merge-base and head
    all_changed_files = deps.git_diff_service.get_changed_files(
        context.merge_base_sha, context.head_sha
    )

    # 2. Filter files according to scope & exclusions
    active_changed_files: list[ChangedFile] = []
    code_facts: list[CodeFact] = []

    for cf in all_changed_files:
        primary_path = cf.path_after or cf.path_before or ""

        # Check exclusions
        if path_matches_globs(primary_path, context.exclude_globs):
            warnings.append(f"Excluded file: {primary_path}")
            continue

        active_changed_files.append(cf)

        # If Python file, extract code facts
        if path_matches_globs(primary_path, context.source_globs):
            before_content = (
                deps.git_snapshot_service.read_file(context.merge_base_sha, cf.path_before)
                if cf.path_before
                else None
            )
            after_content = (
                deps.git_snapshot_service.read_file(context.head_sha, cf.path_after)
                if cf.path_after
                else None
            )

            file_facts = compare_python_facts(
                path=primary_path,
                before_source=before_content,
                after_source=after_content,
            )
            code_facts.extend(file_facts)

    # 3. Extract documentation spans from HEAD snapshot for markdown files
    # We find documentation files present in HEAD or changed in PR
    doc_spans: list[DocSpan] = []
    # Any changed doc file
    for cf in active_changed_files:
        p = cf.path_after or ""
        if p and path_matches_globs(p, context.docs_globs):
            content = deps.git_snapshot_service.read_file(context.head_sha, p)
            if content:
                doc_spans.extend(deps.markdown_extractor.extract(p, content))

    # Also check existing docs in repo working tree/HEAD that match docs_globs
    for glob_pattern in context.docs_globs:
        for doc_file in context.repo_root.glob(glob_pattern):
            if doc_file.is_file():
                rel_path = str(doc_file.relative_to(context.repo_root)).replace("\\", "/")
                if not path_matches_globs(rel_path, context.exclude_globs):
                    # If not already extracted
                    if not any(s.path == rel_path for s in doc_spans):
                        content = deps.git_snapshot_service.read_file(context.head_sha, rel_path)
                        if content:
                            doc_spans.extend(deps.markdown_extractor.extract(rel_path, content))

    # 4. Candidate mapping
    candidates = deps.candidate_mapper.map(code_facts, doc_spans)

    # 5. Deterministic rule evaluation
    deterministic_findings = deps.rule_engine.evaluate(code_facts, doc_spans, candidates)

    existing_keys = {
        (
            f.rule_id,
            f.evidence[0].path if f.evidence else "",
            f.evidence[1].path if len(f.evidence) > 1 else "",
        )
        for f in deterministic_findings
    }

    # 6. Optional AI verifier for remaining behavioral candidates
    ai_findings = []
    if context.model_enabled:
        ai_findings = deps.model_verifier.verify_candidates(
            code_facts, doc_spans, candidates, existing_keys
        )

    all_raw_findings = deterministic_findings + ai_findings

    # 7. Evidence validation trust boundary
    validated_findings = deps.evidence_validator.validate_findings(
        all_raw_findings, context.head_sha
    )

    duration_ms = int((time.perf_counter() - start_time) * 1000)

    drift_count = sum(1 for f in validated_findings if f.status == "DRIFT")
    potential_count = sum(1 for f in validated_findings if f.status == "POTENTIAL_DRIFT")
    uncertain_count = sum(1 for f in validated_findings if f.status == "UNCERTAIN")

    report = ScanReport(
        schema_version="1.0",
        scan_id=context.scan_id,
        base_sha=context.base_sha,
        head_sha=context.head_sha,
        merge_base_sha=context.merge_base_sha,
        tool_version=context.tool_version,
        model_id="organizer-open-weight-verifier" if context.model_enabled else None,
        summary={
            "changed_files": len(active_changed_files),
            "code_facts": len(code_facts),
            "doc_spans": len(doc_spans),
            "findings": len(validated_findings),
            "drift": drift_count,
            "potential_drift": potential_count,
            "uncertain": uncertain_count,
        },
        changed_files=active_changed_files,
        findings=validated_findings,
        warnings=warnings,
        duration_ms=duration_ms,
    )

    return report
