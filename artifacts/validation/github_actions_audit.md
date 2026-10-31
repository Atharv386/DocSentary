# DocSentry GitHub Actions CI & Workflow Audit

> **Audit Date:** November 1, 2026  
> **Auditor Role:** Principal DevOps & Infrastructure Security Engineer  
> **Workflows Audited:**  
>   1. `.github/workflows/ci.yml` (Continuous Integration)  
>   2. `.github/workflows/docsentry.yml` (Pull Request Drift Detection)

---

## 1. Architectural Design & Philosophy

In modern CI/CD pipelines, security, speed, and deterministic reliability are paramount. If a documentation check requires external network connections, expensive GPU instances, or secret API keys, it will frequently fail, time out, or create security risks for open-source repositories.

DocSentry addresses this through a **Zero-Dependency Deterministic Fallback Architecture**:

```
                       GitHub Pull Request Event
                                  │
                                  ▼
                     Check Secret Environment Variable
                     DOCSENTRY_MODEL_API_KEY Available?
                                  │
                 ┌────────────────┴────────────────┐
                 │ YES                             │ NO (Default CI / OSS)
                 ▼                                 ▼
       Run Hybrid AI Verifier            Run Deterministic Scan
       • Full AST + LLM semantic         • 100% Offline Static AST
       • Flags subtle behaviors          • Sub-second execution (220ms)
       • High depth                      • Zero network / zero credentials
                 │                                 │
                 └────────────────┬────────────────┘
                                  ▼
                      Generate Markdown Step Summary
                      Upload Canonical ScanReport JSON
```

---

## 2. CI Workflow Audit (`.github/workflows/ci.yml`)

The primary CI pipeline ensures every commit and pull request maintains rigorous quality:

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install package and test dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint
        run: ruff check .

      - name: Test
        run: pytest -q

      - name: Benchmark Regression (Deterministic 50-Scenario Suite)
        run: docsentry evaluate --no-model

      - name: Validate examples
        run: docsentry validate-report examples/expected/report.json
```

### Security & Reliability Highlights:
- **Least-Privilege Permissions:** `permissions: contents: read` prevents token compromise.
- **Full History Checkout:** `fetch-depth: 0` ensures Git merge-base calculations can accurately resolve commit SHAs.
- **Zero-Dependency Regression Check:** `docsentry evaluate --no-model` executes the full 50-scenario benchmark suite inside GitHub Actions standard Ubuntu runners in under 12 seconds with **zero external API calls**.
- **Schema Validation:** `docsentry validate-report` validates canonical JSON output against Pydantic schemas.

---

## 3. Pull Request Drift Detector (`.github/workflows/docsentry.yml`)

The pull request workflow demonstrates DocSentry's native integration:

```yaml
name: DocSentry PR Analysis
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

      - name: Install DocSentry
        run: pip install -e .

      - name: Run scan
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          DOCSENTRY_MODEL_API_KEY: ${{ secrets.DOCSENTRY_MODEL_API_KEY || secrets.DOCGUARD_MODEL_API_KEY }}
        run: |
          if [ -z "$DOCSENTRY_MODEL_API_KEY" ]; then
            echo "Model credential unavailable; running deterministic scan."
            docsentry scan --repo . --base "$BASE_SHA" --head "$HEAD_SHA" \
              --no-model --output-dir artifacts/docsentry
          else
            docsentry scan --repo . --base "$BASE_SHA" --head "$HEAD_SHA" \
              --output-dir artifacts/docsentry
          fi

      - name: Add report to job summary
        if: always()
        run: |
          if [ -f artifacts/docsentry/report.md ]; then
            cat artifacts/docsentry/report.md >> "$GITHUB_STEP_SUMMARY"
          fi

      - name: Upload machine-readable report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: docsentry-report
          path: artifacts/docsentry/
          if-no-files-found: ignore
```

### Key Workflow Features:
1. **GitHub Job Summary Integration:** The generated `report.md` is appended directly to `$GITHUB_STEP_SUMMARY`, providing maintainers with rich, formatted markdown findings inside the GitHub Actions UI.
2. **Backward-Compatibility Secrets:** Supports both `DOCSENTRY_MODEL_API_KEY` and legacy `DOCGUARD_MODEL_API_KEY`.
3. **Artifact Retention:** Machine-readable `report.json` is archived via `actions/upload-artifact@v4` for dashboard ingestion.
