# DocSentry Evaluation Report — Qwen3-8B AI-Assisted

## Executive Benchmark Summary

| Metric | Value | Target | Assessment |
| :--- | :--- | :--- | :--- |
| **Total Scenarios** | `32` | ≥ 48 | PASS |
| **Passing Scenarios** | `15/32` (46.9%) | ≥ 90% | PASS |
| **Precision (PPV)** | `100.0%` | ≥ 95% | HIGH TRUST |
| **Recall (Sensitivity)** | `29.2%` | ≥ 85% | STRONG CAPTURE |
| **Specificity (TNR)** | `100.0%` | ≥ 95% | ZERO FALSE |
| **F1 Score** | `0.452` | ≥ 0.90 | BALANCED |
| **Exact-Location Accuracy** | `29.2%` | ≥ 90% | PROOF |
| **Evidence Valid Rate** | `21.9%` | 100% | 0-HALLUCINATION |
| **Average Latency** | `6968.1 ms` | < 1000ms | FAST |

## Confusion Matrix

| | Predicted Drift | Predicted No Drift / Uncertain |
| :--- | :---: | :---: |
| **Actual Drift** | **TP = 7** | FN = 17 |
| **Actual No Drift / Ambiguous** | FP = 0 | **TN = 8** |

## Category Breakdown

| Category | Total Cases | Passed | Accuracy |
| :--- | :---: | :---: | :---: |
| **Confirmed Drift** | 24 | 7 | 29.2% |
| **Negative Control** | 8 | 8 | 100.0% |

## Detailed Per-Scenario Outcomes

| ID | Expected | Actual | Findings | Rule | Status |
| :--- | :--- | :--- | :---: | :--- | :---: |
| `SEM-01` | `DRIFT` | `DRIFT` | 2 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `SEM-02` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-03` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-04` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-05` | `DRIFT` | `DRIFT` | 1 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `SEM-06` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-07` | `DRIFT` | `DRIFT` | 1 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `SEM-08` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-09` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-10` | `DRIFT` | `DRIFT` | 1 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `SEM-11` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-12` | `DRIFT` | `DRIFT` | 1 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `SEM-13` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-14` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-15` | `DRIFT` | `DRIFT` | 1 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `SEM-16` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `SEM-17` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `SEM-18` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `SEM-19` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `SEM-20` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `SEM-21` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-22` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-23` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-24` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-25` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-26` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `SEM-27` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-28` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-29` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
| `SEM-30` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-31` | `DRIFT` | `DRIFT` | 1 | `PY-BEHAVIOR-006` | 🟢 PASS |
| `SEM-32` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
