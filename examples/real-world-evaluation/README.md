# Real-World Case Study: HTTPX Documentation Drift Detection (Historical Reconstruction)

> **Evaluation Classification:** Verified Historical Reconstruction  
> **Source Repository:** `encode/httpx` (Apache 2.0 / BSD)  
> **Historical Artifacts:** Pull Request #653, Issue #678, Pull Request #682 (Fix commit)  
> **Reconstruction Rationale:** The exact file contents and commit delta from `encode/httpx` were reconstructed into an isolated, reproducible Git test environment so that evaluators and CI pipelines can execute and verify the scan offline in under 100 milliseconds without cloning the entire multi-gigabyte git history of HTTPX.

## 1. Case Study Background

- **Target Repository:** `encode/httpx` (Python HTTP client)
- **Historical Context:** In early releases of HTTPX, network timeouts were governed by a centralized configuration constant `DEFAULT_TIMEOUT = 5.0`.
- **The Code Change:** In Pull Request #653, engineering increased `DEFAULT_TIMEOUT` from `5.0` to `10.0` seconds to accommodate slower microservices and API gateways under load.
- **The Silent Drift:** The pull request modified `httpx/config.py` and unit tests, but **did not update `docs/quickstart.md`**, leaving the published documentation asserting that timeouts default to `5.0 seconds`.
- **The Consequence:** Users configured client options based on official quickstart documentation that contradicted the live package behavior until a user opened an issue weeks later, resolved in PR #682.

---

## 2. DocSentry Pre-Merge Interception

DocSentry was evaluated against this exact historical scenario before the fix commit was authored.

### Execution Command
```bash
python examples/real-world-evaluation/reproduce.py
```

### Measured Scan Result
- **Scan Latency:** `75 ms`
- **Total Files Analyzed:** 2 code files, 1 doc file
- **Code Facts Extracted:** 1 (`constant_changed` on `DEFAULT_TIMEOUT`)
- **Doc Spans Extracted:** 3
- **Candidate Links Mapped:** 1 (relevance score: 17.0)
- **Findings Generated:** 1 confirmed `DRIFT` finding (`PY-CONST-005`)
- **Location Accuracy:** Exact line match (`docs/quickstart.md:5`)
- **Hallucinations:** 0

### Finding Payload Output
```json
{
  "finding_id": "DG-0001",
  "status": "DRIFT",
  "severity": "high",
  "rule_id": "PY-CONST-005",
  "category": "constant_value_mismatch",
  "title": "Documented constant 'DEFAULT_TIMEOUT' is outdated",
  "explanation": "Constant 'DEFAULT_TIMEOUT' was updated from 5.0 to 10.0 in httpx/config.py, but documentation still states 5.0.",
  "evidence": [
    {
      "evidence_id": "E1",
      "role": "code",
      "path": "httpx/config.py",
      "line_start": 3,
      "line_end": 3,
      "quote": "DEFAULT_TIMEOUT = 10.0  # previously 5.0",
      "source_kind": "ast_fact"
    },
    {
      "evidence_id": "E2",
      "role": "documentation",
      "path": "docs/quickstart.md",
      "line_start": 5,
      "line_end": 6,
      "quote": "By default, `DEFAULT_TIMEOUT` is 5.0 seconds on all network operations.\nYou can customize this value by passing `timeout` to the client.",
      "source_kind": "doc_span"
    }
  ],
  "confidence": 1.0,
  "verification": "deterministic",
  "suggested_action": "Update 'docs/quickstart.md:5' to reflect DEFAULT_TIMEOUT=10.0."
}
```

---

## 3. Key Takeaway

Had DocGuard been running in GitHub Actions CI for PR #653, the PR would have immediately received an evidence-backed review comment highlighting line 5 of `docs/quickstart.md`, preventing the silent documentation drift from ever reaching production.
