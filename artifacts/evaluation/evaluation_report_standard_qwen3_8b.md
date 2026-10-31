# DocSentry Evaluation Report — Qwen3-8B AI-Assisted

## Executive Benchmark Summary

| Metric | Value | Target | Assessment |
| :--- | :--- | :--- | :--- |
| **Total Scenarios** | `50` | ≥ 48 | PASS |
| **Passing Scenarios** | `45/50` (90.0%) | ≥ 90% | PASS |
| **Precision (PPV)** | `90.0%` | ≥ 95% | HIGH TRUST |
| **Recall (Sensitivity)** | `90.0%` | ≥ 85% | STRONG CAPTURE |
| **Specificity (TNR)** | `93.3%` | ≥ 95% | ZERO FALSE |
| **F1 Score** | `0.900` | ≥ 0.90 | BALANCED |
| **Exact-Location Accuracy** | `95.0%` | ≥ 90% | PROOF |
| **Evidence Valid Rate** | `44.0%` | 100% | 0-HALLUCINATION |
| **Average Latency** | `1548.5 ms` | < 1000ms | FAST |

## Confusion Matrix

| | Predicted Drift | Predicted No Drift / Uncertain |
| :--- | :---: | :---: |
| **Actual Drift** | **TP = 18** | FN = 2 |
| **Actual No Drift / Ambiguous** | FP = 2 | **TN = 28** |

## Category Breakdown

| Category | Total Cases | Passed | Accuracy |
| :--- | :---: | :---: | :---: |
| **Confirmed Drift** | 14 | 13 | 92.9% |
| **Negative Control** | 14 | 14 | 100.0% |
| **Ambiguous Edge Case** | 12 | 9 | 75.0% |
| **Doc Semantics** | 10 | 9 | 90.0% |

## Detailed Per-Scenario Outcomes

| ID | Expected | Actual | Findings | Rule | Status |
| :--- | :--- | :--- | :---: | :--- | :---: |
| `A-01` | `DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🟢 PASS |
| `A-02` | `DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🟢 PASS |
| `A-03` | `DRIFT` | `DRIFT` | 1 | `PY-PARAM-002` | 🟢 PASS |
| `A-04` | `DRIFT` | `DRIFT` | 1 | `PY-PARAM-002` | 🟢 PASS |
| `A-05` | `POTENTIAL_DRIFT` | `POTENTIAL_DRIFT` | 1 | `PY-SYMBOL-003` | 🟢 PASS |
| `A-06` | `POTENTIAL_DRIFT` | `POTENTIAL_DRIFT` | 1 | `PY-SYMBOL-003` | 🟢 PASS |
| `A-07` | `DRIFT` | `DRIFT` | 1 | `PY-CONFIG-004` | 🟢 PASS |
| `A-08` | `DRIFT` | `DRIFT` | 1 | `PY-CONFIG-004` | 🟢 PASS |
| `A-09` | `DRIFT` | `DRIFT` | 1 | `PY-CONST-005` | 🟢 PASS |
| `A-10` | `DRIFT` | `DRIFT` | 1 | `PY-CONST-005` | 🟢 PASS |
| `A-11` | `DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🟢 PASS |
| `A-12` | `DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🟢 PASS |
| `A-13` | `DRIFT` | `DRIFT` | 1 | `PY-PARAM-002` | 🟢 PASS |
| `A-14` | `DRIFT` | `UNCERTAIN` | 1 | `PY-DEFAULT-001` | 🔴 FAIL |
| `B-01` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-02` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-03` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-04` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-05` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-06` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-07` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-08` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-09` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-10` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-11` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-12` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-13` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `B-14` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `C-01` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `C-02` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `C-03` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `C-04` | `DRIFT` | `DRIFT` | 1 | `PY-CONST-005` | 🟢 PASS |
| `C-05` | `UNCERTAIN` | `DRIFT` | 1 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `C-06` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `C-07` | `UNCERTAIN` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `C-08` | `UNCERTAIN` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `C-09` | `UNCERTAIN` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `C-10` | `NO_DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🔴 FAIL |
| `C-11` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `C-12` | `UNCERTAIN` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `D-01` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `D-02` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `D-03` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `D-04` | `DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🟢 PASS |
| `D-05` | `DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🟢 PASS |
| `D-06` | `DRIFT` | `UNCERTAIN` | 1 | `PY-DEFAULT-001` | 🔴 FAIL |
| `D-07` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `D-08` | `DRIFT` | `DRIFT` | 1 | `PY-DEFAULT-001` | 🟢 PASS |
| `D-09` | `DRIFT` | `DRIFT` | 1 | `PY-CONFIG-004` | 🟢 PASS |
| `D-10` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
