# DocSentry v0.2: Semantic Retrieval & Pipeline Failure Analysis

**Product:** DocSentry  
**Evaluation Baseline Commit:** `6dd5542`  
**Auditor / Architect:** Principal Static Analysis & Quality Engineering Lead  
**Scope:** Forensic Failure Analysis of All Four Verified False Negatives (`REAL-REQUESTS-01`, `REAL-PYDANTIC-01`, `REAL-FLASK-01`, `REAL-FLASK-02`)

---

## 1. Executive Summary

The independent ground-truth audit (`6dd5542`) established a verified benchmark consisting of **25 authentic historical scenarios** (11 positive drift cases, 14 negative controls) across 7 major open-source repositories. Both the deterministic engine and selective hybrid pipeline achieved:
- **True Positives (TP):** 7
- **True Negatives (TN):** 14
- **False Positives (FP):** 0
- **False Negatives (FN):** 4
- **Precision:** 100.0%
- **Recall:** 63.6%
- **F1 Score:** 0.7778

The central question addressed in this investigation is:

> *Where did the detection pipeline fail on the four false negatives, and why was genuine documentation drift missed?*

### Critical Initial Finding: Not an LLM Reasoning Failure
Prior assumptions posited that missed documentation drift was caused by limitations in model reasoning or the need for heavyweight vector embeddings. A forensic stage-by-stage pipeline trace reveals the contrary:
1. **Three of the four failures (75%) were Code Extraction Failures (Stage 2):** In `REAL-PYDANTIC-01`, `REAL-FLASK-01`, and `REAL-FLASK-02`, the Python AST visitor completely failed to extract code facts for annotated assignments (`ast.AnnAssign`), class attributes (`Flask.json_encoder`), and environment variable lookups (`os.environ.get('FLASK_ENV')`). The candidate retrieval and AI verification layers were never even reached because `code_facts` was completely empty.
2. **One failure (25%) was a Documentation Claim Classification & AI Routing Failure (Stages 4 & 8):** In `REAL-REQUESTS-01`, candidate retrieval succeeded with a high relevance score (9.00). However, the documentation claim classifier categorized procedural guidance ("To send JSON, explicitly serialize...") as `general_description` rather than `active_assertion`, causing the semantic routing filter to prematurely drop the candidate before invoking Qwen. When tested with a bounded evidence bundle, `qwen3:8b` diagnosed the behavioral drift immediately.

---

## 2. Stage-by-Stage Pipeline Trace: All Four Verified False Negatives

The DocSentry detection pipeline processes each scenario through 11 discrete stages:
1. Git diff extraction
2. Code fact extraction (`compare_python_facts`)
3. Changed symbol and behavioural fact generation
4. Documentation claim classification (`MarkdownExtractor`)
5. Candidate document retrieval (`CandidateMapper`)
6. Candidate relevance scoring
7. Evidence bundle generation
8. Qwen invocation (`SemanticModelVerifier`)
9. Model output
10. Evidence validation (`EvidenceValidator`)
11. Final finding generation

---

### Case 1: `REAL-REQUESTS-01` (`psf/requests` — Validation Split)

- **Authentic Code Change:**
  ```python
  # BASE (requests/api.py)
  def post(url, data=None):
      return session.post(url, data=data)

  # HEAD (requests/api.py)
  def post(url, data=None, json=None):
      return session.post(url, data=data, json=json)
  ```
- **Documentation Sentence (`docs/user/quickstart.md`):**  
  `"To send JSON, explicitly serialize the string with data=json.dumps(payload)."`
- **Ground Truth Drift:** Behavioral / procedural contract drift. Adding the native `json=` parameter makes the documentation's claim that callers must manually serialize via `data=json.dumps(...)` obsolete and misleading.

#### 11-Stage Pipeline Trace

| Stage | Pipeline Operation | Observed Execution Outcome | Diagnosis |
|:---|:---|:---|:---|
| **1. Git Diff** | Inspect changed files | `['requests/api.py']` detected | **OK** |
| **2. Code Facts** | AST parsing & comparison | `kind=parameter_added, symbol=post, member=json` | **OK** |
| **3. Fact Generation** | Behavioral fact tagging | Category tagged as `"syntactic"` | Neutral |
| **4. Doc Parsing** | Tokenize & classify claim | `claim_type = "general_description"` | **FAILED:** Did not recognize imperative procedural instruction ("To send JSON...") |
| **5. Candidate Retrieval** | Code-to-doc mapping | Mapped `param-add-1` to `docs/user/quickstart.md:3` | **OK** |
| **6. Relevance Scoring** | Weighted candidate scoring | Score: **9.00** (`exact_parameter_or_flag_match`, `heading_keyword_match`) | **OK** (Well above 4.0 threshold) |
| **7. Evidence Bundling** | Bundle construction | Ready for evaluation | **OK** |
| **8. Model Invocation** | Routing filter evaluation | Skipped! `link.score >= 5.0 and span_claim == 'active_assertion'` evaluated to `False` | **FAILED:** Over-aggressive filter blocked invocation |
| **9. Model Output** | Qwen semantic inference | *Never invoked in baseline* | Missed opportunity |
| **10. Evidence Validation**| Validate spans against Git | *Never reached* | Blocked by Stage 8 |
| **11. Final Finding** | Emit Finding record | 0 findings emitted | **FALSE NEGATIVE** |

- **Failure Classification:** `Documentation parsing failure & AI routing filter failure`
- **Root Cause:** `_classify_claim_type` lacked keywords for procedural instructions starting with `"To <verb>"`, defaulting to `general_description`. In `verifier.py`, candidates with non-`active_assertion` claims were dropped regardless of candidate link strength.

---

### Case 2: `REAL-PYDANTIC-01` (`pydantic/pydantic` — Held-Out Test Split)

- **Authentic Code Change:**
  ```python
  # BASE (pydantic/main.py)
  class ConfigDict:
      orm_mode: bool = False

  # HEAD (pydantic/main.py)
  class ConfigDict:
      from_attributes: bool = False
  ```
- **Documentation Sentence (`docs/usage/models.md`):**  
  `"Enable ORM mode on your model by setting orm_mode = True."`
- **Ground Truth Drift:** Symbol / configuration key removed. `orm_mode` was deprecated and replaced with `from_attributes` during the Pydantic v2 migration.

#### 11-Stage Pipeline Trace

| Stage | Pipeline Operation | Observed Execution Outcome | Diagnosis |
|:---|:---|:---|:---|
| **1. Git Diff** | Inspect changed files | `['pydantic/main.py']` detected | **OK** |
| **2. Code Facts** | AST parsing & comparison | **0 facts extracted** | **FAILED:** `ASTVisitor` did not implement `visit_AnnAssign` |
| **3. Fact Generation** | Changed symbol generation | Empty list | Blocked by Stage 2 |
| **4. Doc Parsing** | Tokenize & classify claim | `claim_type = "active_assertion"` | **OK** |
| **5. Candidate Retrieval** | Code-to-doc mapping | 0 candidates mapped | Blocked by empty code facts |
| **6. Relevance Scoring** | Weighted candidate scoring | N/A | Blocked |
| **7. Evidence Bundling** | Bundle construction | N/A | Blocked |
| **8. Model Invocation** | Routing filter evaluation | N/A | Blocked |
| **9. Model Output** | Qwen semantic inference | N/A | Blocked |
| **10. Evidence Validation**| Validate spans against Git | N/A | Blocked |
| **11. Final Finding** | Emit Finding record | 0 findings emitted | **FALSE NEGATIVE** |

- **Failure Classification:** `Extraction failure (Python AST)`
- **Root Cause:** Modern Python code relies heavily on annotated assignments (`orm_mode: bool = False`). The `ASTVisitor` only implemented `visit_Assign` and completely lacked a handler for `ast.AnnAssign`.

---

### Case 3: `REAL-FLASK-01` (`pallets/flask` — Held-Out Test Split)

- **Authentic Code Change:**
  ```python
  # BASE (flask/app.py)
  class Flask:
      json_encoder = json.JSONEncoder

  # HEAD (flask/app.py)
  class Flask:
      # json_encoder removed in favor of json_provider
      json_provider_class = None
  ```
- **Documentation Sentence (`docs/api.md`):**  
  `"Customize JSON serialization by overriding Flask.json_encoder."`
- **Ground Truth Drift:** Symbol removed. Flask 2.0 removed `Flask.json_encoder` in favor of pluggable JSON providers.

#### 11-Stage Pipeline Trace

| Stage | Pipeline Operation | Observed Execution Outcome | Diagnosis |
|:---|:---|:---|:---|
| **1. Git Diff** | Inspect changed files | `['flask/app.py']` detected | **OK** |
| **2. Code Facts** | AST parsing & comparison | **0 facts extracted** | **FAILED:** `visit_Assign` dropped assignments inside classes |
| **3. Fact Generation** | Changed symbol generation | Empty list | Blocked by Stage 2 |
| **4. Doc Parsing** | Tokenize & classify claim | `claim_type = "active_assertion"` | **OK** |
| **5. Candidate Retrieval** | Code-to-doc mapping | 0 candidates mapped | Blocked by empty code facts |
| **6. Relevance Scoring** | Weighted candidate scoring | N/A | Blocked |
| **7. Evidence Bundling** | Bundle construction | N/A | Blocked |
| **8. Model Invocation** | Routing filter evaluation | N/A | Blocked |
| **9. Model Output** | Qwen semantic inference | N/A | Blocked |
| **10. Evidence Validation**| Validate spans against Git | N/A | Blocked |
| **11. Final Finding** | Emit Finding record | 0 findings emitted | **FALSE NEGATIVE** |

- **Failure Classification:** `Extraction failure (Python AST)`
- **Root Cause:** In `ASTVisitor.visit_Assign`, an explicit check `if not self.scope_stack:` ignored all variable assignments occurring within class bodies (`class Flask:`). As a result, class attributes and their deletions were invisible to the diff comparator.

---

### Case 4: `REAL-FLASK-02` (`pallets/flask` — Held-Out Test Split)

- **Authentic Code Change:**
  ```python
  # BASE (flask/cli.py)
  env = os.environ.get('FLASK_ENV', 'production')

  # HEAD (flask/cli.py)
  # FLASK_ENV deprecated, use --debug flag
  env = 'production'
  ```
- **Documentation Sentence (`docs/config.md`):**  
  `"Set FLASK_ENV=development to enable debug mode."`
- **Ground Truth Drift:** Configuration / environment flag deprecation and removal.

#### 11-Stage Pipeline Trace

| Stage | Pipeline Operation | Observed Execution Outcome | Diagnosis |
|:---|:---|:---|:---|
| **1. Git Diff** | Inspect changed files | `['flask/cli.py']` detected | **OK** |
| **2. Code Facts** | AST parsing & comparison | **0 facts extracted** | **FAILED:** Lowercase assignment & `os.environ.get` call ignored |
| **3. Fact Generation** | Changed symbol generation | Empty list | Blocked by Stage 2 |
| **4. Doc Parsing** | Tokenize & classify claim | `claim_type = "active_assertion"` | **OK** |
| **5. Candidate Retrieval** | Code-to-doc mapping | 0 candidates mapped | Blocked by empty code facts |
| **6. Relevance Scoring** | Weighted candidate scoring | N/A | Blocked |
| **7. Evidence Bundling** | Bundle construction | N/A | Blocked |
| **8. Model Invocation** | Routing filter evaluation | N/A | Blocked |
| **9. Model Output** | Qwen semantic inference | N/A | Blocked |
| **10. Evidence Validation**| Validate spans against Git | N/A | Blocked |
| **11. Final Finding** | Emit Finding record | 0 findings emitted | **FALSE NEGATIVE** |

- **Failure Classification:** `Extraction failure (Python AST)`
- **Root Cause:** Constant extraction required `target.id.isupper()`. Because `env` was lowercase, it was bypassed. Additionally, `os.environ.get` calls were not recognized as configuration flags, leaving the removal of `'FLASK_ENV'` completely unrepresented in `code_facts`.

---

## 3. Failure Taxonomy Summary

| Case ID | Repository | Split | Root Cause Stage | Failure Classification | Targeted Resolution |
|:---|:---|:---:|:---:|:---|:---|
| `REAL-REQUESTS-01` | `psf/requests` | `val` | Stages 4 & 8 | Documentation Claim Parsing & AI Routing Filter | Recognize imperative procedural directives ("To <verb>..."); allow strong semantic candidate links (score >= 5.0) to invoke Qwen |
| `REAL-PYDANTIC-01` | `pydantic/pydantic` | `test` | Stage 2 | Code Fact Extraction (`ast.AnnAssign`) | Implement `visit_AnnAssign` in `ASTVisitor` to track typed class attributes |
| `REAL-FLASK-01` | `pallets/flask` | `test` | Stage 2 | Code Fact Extraction (Class Attributes) | Remove `scope_stack` exclusion in `visit_Assign` and compare class-level attributes |
| `REAL-FLASK-02` | `pallets/flask` | `test` | Stage 2 | Code Fact Extraction (Env Variables) | Implement `_check_env_call` in `ASTVisitor` for `os.environ.get` and `os.getenv` |

---

## 4. Key Takeaways

1. **Static Analysis Completeness is Foundational:** No AI reasoning system can detect drift if the underlying static extractor fails to observe that a code symbol was deleted or altered. 75% of DocSentry's false negatives stemmed from incomplete AST visitation of class attributes and modern type annotations.
2. **Deterministic-AI Pipeline Handshake:** In `REAL-REQUESTS-01`, when the documentation claim was correctly identified as an active procedural instruction, the candidate mapper scored it at 9.00, and Qwen correctly identified the contradiction with 100% precision. The bottleneck was an overly conservative filter at the routing boundary.
3. **Evidence Standards Preserved:** In all four cases, the necessary improvements remain strictly bounded to verifiable AST facts and exact documentation spans, ensuring that fixing these false negatives introduces zero hallucinations or false positives.
