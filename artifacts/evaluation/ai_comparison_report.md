# DocGuard Evaluation Report: Deterministic vs. Qwen3-8B AI-Assisted Architecture

**Product:** DocGuard (Automated Documentation Drift Detection)  
**Author:** Founding Engineering Team  
**Date:** November 1, 2026  
**Evaluated Systems:**
- **Configuration A:** Deterministic AST & Line-Span Engine (`--no-model`)
- **Configuration B:** Hybrid Architecture (Deterministic Rules + Local `qwen3:8b` via Ollama at `http://localhost:11434`)

---

## 1. Executive Summary & Core Engineering Finding

In software engineering developer tooling, **precision, predictability, and latency define developer adoption**. A tool that cries wolf on negative controls or takes 15 seconds per PR comment degrades developer trust and gets uninstalled.

Our 50-scenario benchmark suite was designed to test not only drift capture (14 positive cases), but critically **negative controls** (14 cases where docs remain valid), **ambiguous edge cases** (12 dynamic dispatch/overload cases), and **complex documentation semantics** (10 tables, links, code examples).

### Side-by-Side Architectural Benchmark

| Metric | Configuration A (Deterministic Only) | Configuration B (Qwen3-8B Assisted) | Target Standard | Winner |
| :--- | :---: | :---: | :---: | :---: |
| **Total Test Scenarios** | 50 | 50 | ≥ 48 | **Both** |
| **Passing Scenarios** | **43 / 50 (86.0%)** | 38 / 50 (76.0%) | ≥ 80% | **Config A** |
| **Precision (PPV)** | **94.4%** | 73.9% | ≥ 90% | **Config A (+20.5%)** |
| **Recall (Sensitivity)** | **85.0%** | **85.0%** | ≥ 85% | **Tie** |
| **Specificity (TNR)** | **96.7%** | 80.0% | ≥ 95% | **Config A (+16.7%)** |
| **F1 Score** | **0.895** | 0.791 | ≥ 0.85 | **Config A** |
| **Exact-Location Accuracy** | **95.0%** | **95.0%** | ≥ 90% | **Tie** |
| **Evidence Validity Rate** | **100% (Zero Hallucinations)** | **100% (Zero Hallucinations)** | 100% | **Tie** |
| **Average Scan Latency** | **218.9 ms** | 14,652.9 ms (14.6s) | < 1,000 ms | **Config A (67x faster)** |

---

## 2. Deep Dive: Confusion Matrix Analysis

### Configuration A (Deterministic Only)
```
                  Predicted Drift    Predicted No Drift / Uncertain
Actual Drift            17 (TP)                   3 (FN)
Actual No Drift          1 (FP)                  29 (TN)
```
- **False Positives: 1 / 30** (96.7% Specificity). Negative controls achieved **14/14 (100%)** accuracy.
- **False Negatives: 3 / 20**. These are subtle semantic/behavioral changes with no syntactic default change (e.g. `C-04` return value shape change, `A-14` conditional default body).

### Configuration B (Qwen3-8B Hybrid)
```
                  Predicted Drift    Predicted No Drift / Uncertain
Actual Drift            17 (TP)                   3 (FN)
Actual No Drift          6 (FP)                  24 (TN)
```
- **False Positives: 6 / 30** (80.0% Specificity). The LLM introduced 5 additional false alarms.
- **Why did Qwen3-8B introduce False Positives?**
  1. **Negative Controls (B-08, B-12):** When a function changed internally but documentation described general purpose without asserting stale specifics, the LLM over-interpreted the change as requiring doc rewrites.
  2. **Code Examples (D-02):** In user example code (`client.connect(timeout=999)`), the LLM flagged the explicit override as drift against the new default `60`.
  3. **Updated Docs (D-07):** In complex markdown structures with multiple tables, the LLM flagged subtle phrasing changes.

---

## 3. The Evidence Trust Boundary Advantage

Even when Qwen3-8B hallucinated or over-flagged, **DocGuard's Evidence Validation Boundary intercepted every finding**:
- Every cited file path was checked against Git snapshots.
- Every line number was mapped to AST tokens and Markdown CST spans.
- No hallucinated identifiers, non-existent files, or made-up lines were ever permitted to reach the final report.
- **Zero hallucinations reached the user interface in either configuration.**

---

## 4. Production Architectural Recommendation

Based on empirical data from the 50-scenario benchmark:

1. **Default Mode: Deterministic Engine (`--no-model`)**
   - Recommended for CI/CD Pull Request gating.
   - Runs in ~220ms, catches 85% of drift with 94.4% precision and 96.7% specificity.
   - Does not require local GPU/Ollama or paid external API tokens.

2. **Opt-In Mode: Semantic Verifier (`--model`)**
   - Recommended for asynchronous nightly audits, deep doc reviews, or when PRs modify complex business logic with no signature change.
   - Deduplicated through deterministic precedence: deterministic rules evaluate first, and the AI verifier is only invoked on high-confidence candidate links where deterministic rules stayed silent.
