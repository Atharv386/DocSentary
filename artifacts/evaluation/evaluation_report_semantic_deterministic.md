# DocSentry Evaluation Report — Qwen3-8B AI-Assisted

## Executive Benchmark Summary

| Metric | Value | Target | Assessment |
| :--- | :--- | :--- | :--- |
| **Total Scenarios** | `32` | ≥ 48 | PASS |
| **Passing Scenarios** | `8/32` (25.0%) | ≥ 90% | PASS |
| **Precision (PPV)** | `100.0%` | ≥ 95% | HIGH TRUST |
| **Recall (Sensitivity)** | `0.0%` | ≥ 85% | STRONG CAPTURE |
| **Specificity (TNR)** | `100.0%` | ≥ 95% | ZERO FALSE |
| **F1 Score** | `0.000` | ≥ 0.90 | BALANCED |
| **Exact-Location Accuracy** | `0.0%` | ≥ 90% | PROOF |
| **Evidence Valid Rate** | `0.0%` | 100% | 0-HALLUCINATION |
| **Average Latency** | `220.8 ms` | < 1000ms | FAST |

## Confusion Matrix

| | Predicted Drift | Predicted No Drift / Uncertain |
| :--- | :---: | :---: |
| **Actual Drift** | **TP = 0** | FN = 24 |
| **Actual No Drift / Ambiguous** | FP = 0 | **TN = 8** |

## Category Breakdown

| Category | Total Cases | Passed | Accuracy |
| :--- | :---: | :---: | :---: |
| **Confirmed Drift** | 24 | 0 | 0.0% |
| **Negative Control** | 8 | 8 | 100.0% |

## Detailed Per-Scenario Outcomes

| ID | Expected | Actual | Findings | Rule | Status |
| :--- | :--- | :--- | :---: | :--- | :---: |
| `SEM-01` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-02` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-03` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-04` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-05` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-06` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-07` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-08` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-09` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-10` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-11` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-12` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-13` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-14` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-15` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
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
| `SEM-31` | `DRIFT` | `NO_DRIFT` | 0 | - | 🔴 FAIL |
| `SEM-32` | `NO_DRIFT` | `NO_DRIFT` | 0 | - | 🟢 PASS |
