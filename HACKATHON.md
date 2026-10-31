# Hacktoberfest 2026 — Problem Statement 5 (PS5)
## DocGuard: Automated Documentation Drift Detection

### Project Overview
DocGuard is a pull-request-aware documentation consistency analyzer. It inspects the change between a pull request base and head, extracts externally relevant code facts, locates documentation that refers to those facts, detects contradictions or stale references, and publishes findings with traceable evidence.

### Core Architecture
- **Git Diff & Snapshot Engine**: Subprocess Git integration comparing merge-base to head commits without executing repository code.
- **Python AST Extractor**: Analyzes signatures, defaults, constants, and CLI flags via Python `ast`.
- **Markdown Extractor**: Preserves token source maps and computes exact 1-based inclusive line numbers for headings, paragraphs, tables, and code fences via `markdown-it-py`.
- **Candidate Mapper**: Heuristic weighted relevance scoring mapping changed code facts to document spans.
- **Deterministic Rule Engine**: Prioritized checks (`PY-DEFAULT-001`, `PY-PARAM-002`, `PY-SYMBOL-003`, `PY-CONFIG-004`, `PY-CONST-005`).
- **Bounded Model Verifier**: Optional open-weight model integration operating exclusively on bounded evidence bundles with zero hallucination trust boundaries.
- **Evidence Validator**: Re-opens source snapshots to verify every quoted line and character offset before emitting a finding.
- **Outputs**: Canonical `report.json` and human-readable `report.md` for GitHub Step Summaries and developer terminals.
- **Web Dashboard**: Modern, dark-first developer UI for inspecting side-by-side evidence.

### Tool & Model Disclosures
- **Product Model Transport**: Open-weight model adapter interface (`DOCGUARD_MODEL_PROVIDER=organizer_server`). Deterministic rules run first and function completely with `--no-model`.
- **License**: MIT License.
