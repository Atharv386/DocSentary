<div align="center">

# DocGuard
### *Your code evolves. Your documentation should keep up.*

[![CI](https://github.com/Atharv386/DocSentary/actions/workflows/ci.yml/badge.svg)](https://github.com/Atharv386/DocSentary/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://python.org)
[![PR Analysis](https://img.shields.io/badge/GitHub%20Actions-PR%20Drift%20Detector-green.svg)](.github/workflows/docguard.yml)

**Catch documentation drift in pull requests before it reaches production.**

[Overview](#-the-problem) • [How It Works](#-how-it-works) • [Supported Checks](#-supported-checks) • [CLI Quickstart](#-cli-quickstart) • [GitHub Actions](#-github-actions-workflow) • [Architecture](#-architecture) • [Evaluation](#-evaluation--historical-replay)

</div>

---

## 🔍 The Problem

Documentation silently becomes incorrect as software evolves.

A developer updates a parameter's default value (`timeout: int = 30` ➔ `60`), removes an obsolete argument, renames a CLI flag, or modifies configuration keys. The code gets merged, but the documentation is left unchanged. The result is documentation that looks trustworthy but actively misleads developers.

Standard linters only verify markdown formatting and broken links. **DocGuard proves whether your documentation statements are still true after a code change.**

---

## 🛡️ The DocGuard Guarantee: Zero-Hallucination Evidence

Every single drift finding detected by DocGuard provides an immutable, verifiable link between the code change and the outdated sentence:

```
[OUTDATED DOCUMENTATION]                                [ACTUAL CODE CHANGE]
docs/config.md:23                                       src/client.py:12
-------------------------------------------------       -------------------------------------------------
"The default timeout is 30 seconds."               ➔    def connect(..., timeout=60): ...
```

- **Trust before intelligence:** Every finding must cite the exact documentation file, line span, code file, symbol, and diff evidence.
- **Deterministic-first:** Numerical defaults, signatures, CLI flags, and constants are verified using Python AST and Markdown source maps.
- **Bounded semantic verifier:** Open-weight model inference is strictly bounded to candidate evidence packs. Hallucinated lines or quotes are systematically rejected by our evidence validation trust boundary.

---

## ⚡ Supported Checks

| Rule ID | Category | Detection Condition | Default Status |
| :--- | :--- | :--- | :--- |
| `PY-DEFAULT-001` | **Stale Default** | Parameter default changed in AST, but docs still bind the old literal | `DRIFT` |
| `PY-PARAM-002` | **Stale Parameter** | Parameter removed or renamed, but docs still reference it | `DRIFT` / `POTENTIAL_DRIFT` |
| `PY-SYMBOL-003` | **Removed Symbol** | Function/class removed, but docs still instruct users to invoke it | `POTENTIAL_DRIFT` |
| `PY-CONFIG-004` | **Stale Flag / Key** | CLI flag or config key modified, docs table retains old flag | `DRIFT` |
| `PY-CONST-005` | **Stale Constant** | Literal constant value updated, docs retain old value | `DRIFT` |
| `PY-BEHAVIOR-006` | **Behavioral Drift** | Semantic prose change analyzed via bounded open-weight model | `UNCERTAIN` / `POTENTIAL_DRIFT` |

---

## 🚀 CLI Quickstart

### Installation

```bash
# Clone the repository
git clone https://github.com/Atharv386/DocSentary.git
cd DocSentary

# Create virtual environment & install
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Analyze a Pull Request / Local Commits

```bash
# Scan between base commit and head commit
docguard scan --repo . --base <BASE_SHA> --head <HEAD_SHA> --output-dir .docguard

# Run deterministic checks only (no API key needed)
docguard scan --repo . --base <BASE_SHA> --head <HEAD_SHA> --no-model

# Validate a generated ScanReport JSON artifact
docguard validate-report .docguard/report.json

# Execute the comprehensive 50-scenario evaluation benchmark suite
docguard evaluate --no-model

# Execute the 50-scenario benchmark with local Qwen3-8B (Ollama)
docguard evaluate

# Run the real-world HTTPX PR #653 evaluation case study
python examples/real-world-evaluation/reproduce.py

# Execute the historical replay evaluation suite
docguard replay --manifest examples/history/replay.json
```

---

## 🔬 Benchmark & Real-World Evaluation

DocGuard has been evaluated against a comprehensive **50-scenario benchmark suite** across 4 categories:
1. **Category A (14 Confirmed Drift Cases):** Stale defaults, removed parameters, renamed CLI flags, modified constants.
2. **Category B (14 Negative Control Cases):** Docs updated in same PR, internal helpers, unchanged siblings, historical releases.
3. **Category C (12 Ambiguous Edge Cases):** Dynamic reflection, `@typing.overload`, conditional defaults, kwargs forwarding.
4. **Category D (10 Complex Semantics Cases):** Multi-column markdown tables, URL links, code blocks, duplicate sentences.

### Measured Benchmark Performance

| Evaluation Metric | Configuration A (Deterministic Only) | Configuration B (Qwen3-8B Hybrid) |
| :--- | :---: | :---: |
| **Pass Rate** | **43 / 50 (86.0%)** | 38 / 50 (76.0%) |
| **Precision (PPV)** | **94.4%** | 73.9% |
| **Recall (Sensitivity)** | **85.0%** | **85.0%** |
| **Specificity (TNR)** | **96.7%** | 80.0% |
| **F1 Score** | **0.895** | 0.791 |
| **Location Accuracy** | **95.0%** | **95.0%** |
| **Evidence Hallucinations** | **0% (Guaranteed)** | **0% (Guaranteed)** |
| **Average Scan Latency** | **218.9 ms** | 14,652.9 ms |

### Real-World Case Study: HTTPX PR #653

DocGuard was tested on the real-world historical regression in `encode/httpx` PR #653, where `DEFAULT_TIMEOUT` was doubled from 5.0s to 10.0s in code, but `docs/quickstart.md` was overlooked. DocGuard caught the exact stale sentence on line 5 in **75 ms** with 100% confidence. See `examples/real-world-evaluation/` for full details.

---

## 🤖 GitHub Actions Workflow

Integrate DocGuard directly into your CI pipeline using `.github/workflows/docguard.yml`:

```yaml
name: DocGuard PR Analysis
on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install DocGuard
        run: pip install -e .

      - name: Run scan
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          DOCGUARD_MODEL_API_KEY: ${{ secrets.DOCGUARD_MODEL_API_KEY }}
        run: |
          docguard scan --repo . --base "$BASE_SHA" --head "$HEAD_SHA" \
            --output-dir artifacts/docguard

      - name: Publish Step Summary
        if: always()
        run: |
          if [ -f artifacts/docguard/report.md ]; then
            cat artifacts/docguard/report.md >> "$GITHUB_STEP_SUMMARY"
          fi
```

---

## 🏗️ Architecture

```
GitHub PR / CLI (base_sha, head_sha)
         │
         ▼
    ScanContext ───► Git Runner (merge-base, diff, snapshots)
         │                    │
         ├────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  Python AST Facts     DocSpan Parser       Raw Diff Hunks
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                     Candidate Mapper
                   (Weighted Relevance)
                              │
                              ▼
                  Deterministic Rule Engine
                 (PY-DEFAULT, PY-PARAM, etc.)
                              │
                              ▼
                 Bounded Model Verifier (AI)
                  (Open-Weight Protocol)
                              │
                              ▼
                  Evidence Validator Gate
                 (Zero Hallucination Proof)
                              │
                              ▼
                  ScanReport (JSON & Markdown)
```

---

## 📊 Evaluation & Historical Replay

DocGuard includes a validated evaluation dataset (`examples/history/replay.json`) containing 8 test scenarios:

1. **F-01 (stale-default)**: Default parameter change `30` ➔ `60` (`DRIFT`)
2. **F-02 (parameter-added)**: New parameter `retries` added (`POTENTIAL_DRIFT`)
3. **F-03 (removed-symbol)**: Function `old_login` removed (`POTENTIAL_DRIFT`)
4. **F-04 (renamed-flag)**: CLI flag `--timeout` ➔ `--request-timeout` (`DRIFT`)
5. **F-05 (no-doc-impact)**: Internal refactor with unchanged public interface (`NO FINDING`)
6. **F-06 (docs-fixed-same-pr)**: Simultaneous code and documentation update (`NO FINDING`)
7. **F-07 (ambiguous-runtime)**: Dynamic reflection (`UNCERTAIN`)
8. **F-08 (historical-fix)**: Historical evaluation of pre-fix commits (`DRIFT`)

Run the full replay evaluation with:
```bash
docguard replay --manifest examples/history/replay.json
```

---

## ⚙️ Configuration (`docguard.yml`)

```yaml
version: 1
scope:
  source_globs: ["**/*.py"]
  docs_globs: ["**/*.md", "**/*.mdx"]
  exclude_globs:
    - "**/.venv/**"
    - "**/build/**"
    - "**/dist/**"
limits:
  max_files: 250
  max_file_bytes: 500000
  max_doc_spans_per_fact: 5
model:
  enabled: true
  timeout_seconds: 30
report:
  include_no_drift: false
  include_uncertain: true
  fail_on: never
```

---

## ⚖️ License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
