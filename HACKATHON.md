# Hacktoberfest 2026 — Problem Statement 5 (PS5)
## DocGuard: Production-Grade Automated Documentation Drift Detection

### Project Overview
DocGuard is a production-grade developer platform that detects documentation drift in GitHub pull requests before it reaches production. It inspects the change between a pull request base and head, extracts externally relevant code facts, locates documentation that refers to those facts, detects contradictions or stale references, and publishes findings with traceable, zero-hallucination evidence.

---

### Core Architecture & Engineering Highlights
- **Safe Static Analysis:** Zero repository code execution. Fully static Python AST extraction + GFM Markdown parsing with line-accurate spans.
- **Git Diff & Snapshot Services:** Computes true merge-base, name-status, and unified diff hunks, reading file snapshots directly from Git object storage without touching disk checkout.
- **Deterministic-First Rule Engine:**
  - `PY-DEFAULT-001`: Stale default parameters in functions and methods
  - `PY-PARAM-002`: Removed or renamed public parameters
  - `PY-SYMBOL-003`: Removed or renamed public functions and classes
  - `PY-CONFIG-004`: Renamed CLI flags and argument parser options
  - `PY-CONST-005`: Modified configuration constants
- **Bounded Semantic Verifier (`qwen3:8b` via Ollama):**
  - Runs locally at `http://localhost:11434` with zero external API dependencies.
  - Strict evidence bundles: LLM only receives exact code diff and doc span.
  - Deterministic precedence: Deterministic rules evaluate first; LLM only evaluates unhandled semantic candidates.
- **Zero-Hallucination Trust Boundary (`EvidenceValidator`):**
  - Every finding's file path, line numbers, and quoted content are checked against actual Git snapshots.
  - Hallucinated paths, line numbers, or quotes are rejected or downgraded before reaching output.
- **Developer-First Web Dashboard (React 18 + Vite + Tailwind):**
  - Synchronized side-by-side Evidence Inspector with line gutter highlighting.
  - Copyable snippets with visual confirmation.
  - Clear provenance badges (`DETERMINISTIC`, `QWEN3-8B VERIFIED`, `EVIDENCE VALIDATED`).
  - Preloaded with real-world open-source case studies and benchmark scenarios.

---

### Quantitative Evaluation Benchmark (50 Scenarios)

DocGuard was evaluated on an extensive 50-scenario benchmark suite covering 4 distinct categories:
- **Category A (14 Confirmed Drift):** Stale defaults, removed params, renamed flags, constants.
- **Category B (14 Negative Controls):** Docs updated in same PR, internal helpers, sibling methods, historical docs.
- **Category C (12 Ambiguous Edge Cases):** Dynamic dispatch, `@typing.overload`, kwargs forwarding.
- **Category D (10 Complex Semantics):** Markdown tables, external links, duplicate phrases.

| Metric | Configuration A (Deterministic Only) | Configuration B (Qwen3-8B Hybrid) |
| :--- | :---: | :---: |
| **Pass Rate** | **43 / 50 (86.0%)** | 38 / 50 (76.0%) |
| **Precision (PPV)** | **94.4%** | 73.9% |
| **Recall (Sensitivity)** | **85.0%** | **85.0%** |
| **Specificity (TNR)** | **96.7%** | 80.0% |
| **F1 Score** | **0.895** | 0.791 |
| **Location Accuracy** | **95.0%** | **95.0%** |
| **Evidence Hallucinations** | **0% (Zero)** | **0% (Zero)** |
| **Average Latency** | **218.9 ms** | 14,652.9 ms |

---

### Real-World Open-Source Case Study: HTTPX PR #653

DocGuard was evaluated against the historical regression in `encode/httpx` PR #653, where `DEFAULT_TIMEOUT = 5.0` was doubled to `10.0` seconds in `httpx/config.py`, but `docs/quickstart.md` was missed.
- **Execution:** `python examples/real-world-evaluation/reproduce.py`
- **Detection Result:** Caught in **75 ms** with 100% confidence on line 5 of `docs/quickstart.md`.
- **Finding Rule:** `PY-CONST-005` (Constant value mismatch).

---

### Step-by-Step Verification Guide

```bash
# 1. Run all unit and integration tests (32/32 tests)
pytest -v

# 2. Run Ruff static analysis (0 errors)
ruff check .

# 3. Run the 50-scenario deterministic benchmark (218ms, 94.4% precision)
docguard evaluate --no-model

# 4. Run the 50-scenario benchmark with local Qwen3-8B (Ollama)
docguard evaluate

# 5. Run the HTTPX real-world case study
python examples/real-world-evaluation/reproduce.py

# 6. Build the web dashboard
cd web && npm run build
```

---

### License & Compliance
- **License:** MIT License
- **Dependencies:** `pydantic>=2`, `typer`, `rich`, `markdown-it-py`, `httpx`
- **Model Support:** Native Ollama endpoint (`http://localhost:11434`) and OpenAI-compatible `/v1` endpoints.
