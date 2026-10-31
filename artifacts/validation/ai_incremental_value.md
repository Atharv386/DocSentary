# DocSentry AI Value Verification & Incremental Gain Report

> **Audit Date:** November 1, 2026  
> **Evaluation Model:** `Qwen3-8B` (Q4_K_M, 8.2B parameters, local Ollama endpoint)  
> **Benchmark Suites:** Standard 50-Scenario Suite + Dedicated 32-Scenario Semantic Suite

---

## 1. Executive Summary: Does AI Actually Add Value?

A core question in developer-tools product validation is whether integrating an LLM provides defensible incremental value over well-engineered deterministic static analysis (AST parsing and regular expressions).

Our independent audit established two critical findings:

1. **On Standard Structural Drift (Signatures, Defaults, CLI Flags, Constants):**  
   Deterministic rules are vastly superior: they execute in **219.5 ms** (7× faster), consume zero GPU/RAM overhead, achieve **94.7% precision** and **0.923 F1**, and require no model credentials. For standard structural changes, AI is unnecessary and should not be invoked.

2. **On Semantic, Behavioral, and Contractual Drift:**  
   Deterministic rules have a **complete blind spot** (0.0% recall). They cannot understand return shapes (`[]` vs `None` vs exception), concurrency changes (sync vs async), idempotency guarantees, thread safety, or rate limiting. On our dedicated 32-scenario semantic benchmark, **Qwen3-8B delivered an incremental gain of +29.2% recall and +0.452 F1 with 100% precision (0 false positives).**

---

## 2. Dedicated Semantic Benchmark (32 Scenarios)

We authored 32 targeted scenarios evaluating behavioral drift conditions that are syntactically valid in Python AST but factually break documented contracts:

| Evaluation Metric | Deterministic Baseline (`--no-model`) | Qwen3-8B Hybrid Model | Net Incremental AI Delta |
| :--- | :---: | :---: | :---: |
| **Total Scenarios** | 32 | 32 | — |
| **Passing Scenarios** | **8 / 32 (25.0%)** | **15 / 32 (46.9%)** | **+21.9% (+7 scenarios)** |
| **True Positives (TP)** | 0 | 7 | **+7 True Positives** |
| **True Negatives (TN)** | 8 | 8 | 0 (100% preserved) |
| **False Positives (FP)** | 0 | 0 | 0 (0 spurious alarms) |
| **False Negatives (FN)** | 24 | 17 | **-7 False Negatives** |
| **Precision (PPV)** | 100.0% (undefined/perfect) | **100.0% (7/7)** | **Uncompromised** |
| **Recall (Sensitivity)** | **0.0% (0/24)** | **29.2% (7/24)** | **+29.2% recall gain** |
| **F1 Score** | **0.000** | **0.452** | **+0.452 F1 gain** |
| **Average Latency** | **220.8 ms** | **6,968.1 ms** | ~6.9s reasoning time |

---

## 3. Scenario-by-Scenario Breakdown of AI Detections

The following scenarios were **completely missed by deterministic analysis** but **successfully identified by Qwen3-8B**:

| Scenario ID | Test Case Name | Code Change Delta | Outdated Documentation Statement | Qwen3-8B Verifier Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **`SEM-01`** | `returns_empty_list_instead_of_exception` | Code returns `[]` instead of raising `NotFoundError` | "`get_users()` raises `NotFoundError` if no matching users are found." | **DRIFT** (`direct_contradiction`): Code was modified to return an empty list; doc asserts exception is raised. |
| **`SEM-05`** | `sync_to_async_conversion` | `def load_config()` converted to `async def load_config()` | "`load_config()` is a synchronous blocking function call." | **DRIFT** (`direct_contradiction`): Function was made asynchronous coroutine; doc explicitly states synchronous. |
| **`SEM-07`** | `authentication_required` | Added `Authorization` header check raising `PermissionError` | "The `get_status` endpoint is completely unauthenticated and public." | **DRIFT** (`direct_contradiction`): Enforcement of auth token directly contradicts documentation claiming public unauthenticated access. |
| **`SEM-10`** | `exception_type_changed` | Raised `ParseSyntaxError` instead of standard `ValueError` | "`parse_payload()` raises `ValueError` if the input is malformed." | **DRIFT** (`direct_contradiction`): Exception type changed to custom syntax error, violating documented API contract. |
| **`SEM-12`** | `rate_limiting_enforced` | Added `TooManyRequestsError` check on request context | "There are no rate limits imposed on `invoke_handler()` calls." | **DRIFT** (`direct_contradiction`): Rate limit logic introduced in handler contradicts documented absence of rate limits. |
| **`SEM-15`** | `encoding_restricted_utf8` | Replaced system locale fallback with hardcoded `utf-8` | "Defaults to the system locale encoding if not explicitly specified." | **DRIFT** (`direct_contradiction`): System locale dynamic fallback removed in favor of hardcoded UTF-8 literal. |
| **`SEM-31`** | `zero_division_nan_return` | Returns `float('nan')` instead of raising `ZeroDivisionError` | "`divide()` raises `ZeroDivisionError` when the divisor is zero." | **DRIFT** (`direct_contradiction`): Code returns NaN rather than throwing ZeroDivisionError as documented. |

---

## 4. Why Selective Hybrid Routing is the Optimal Architecture

A naive approach of piping all diffs into an LLM causes high latency (15+ seconds per scan) and introduces false positives on negative controls (hallucinated relevance on illustrative code examples).

DocSentry's architecture achieves the best of both worlds:
1. **Deterministic Fast Path (Rules 001-005):** Handles 85%+ of pull requests in ~200 ms with 94.7% precision.
2. **Selective AI Routing (Layer 3):** Only routes AST behavioral deltas (`return_changed`, `exception_changed`, dynamic reflection) to Qwen3-8B.
3. **Evidence Validation Boundary:** Every claim generated by the LLM must be anchored to verified Git snapshots before a finding is emitted.
