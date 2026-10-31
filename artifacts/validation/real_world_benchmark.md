# DocSentry Real-World Historical Benchmark Report

> **Evaluation Environment:** Real-world historical Git commit reconstructions
> **Evaluator:** DocSentry Independent Replay Harness
> **Strict Policy:** Repository-level partitioning (Dev, Validation, Held-out Test)

## 1. Multi-Configuration Comparative Performance

| Metric | Deterministic-Only | Qwen3-8B-Only | Selective Hybrid |
| :--- | :---: | :---: | :---: |
| **Total Cases** | 32 | 32 | 32 |
| **Pass Rate** | 24/32 (75.0%) | N/A | N/A |
| **Precision (PPV)** | 100.0% | N/A | **N/A** |
| **Recall (Sensitivity)** | 55.6% | N/A | **N/A** |
| **Specificity (TNR)** | 100.0% | N/A | **N/A** |
| **F1 Score** | 0.714 | N/A | **N/A** |
| **Location Accuracy** | 55.6% | N/A | **N/A** |
| **Code Attribution** | 55.6% | N/A | **N/A** |
| **Average Latency** | **213.3 ms** | N/A ms | N/A ms |
| **Model Invocations** | 0 | N/A | N/A |

## 2. Confusion Matrices (Raw Counts)

| Configuration | True Positives | True Negatives | False Positives | False Negatives |
| :--- | :---: | :---: | :---: | :---: |
| `deterministic` | 10 | 14 | 0 | 8 |

## 3. Per-Repository Breakdown (Selective Hybrid)

| Repository | Split | Total | Passed | Pass Rate |
| :--- | :---: | :---: | :---: | :---: |
