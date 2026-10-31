from docguard.evaluation.models import EvaluationCase


def get_all_evaluation_cases() -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []

    # =========================================================================
    # CATEGORY A: Confirmed Positive Drift (14 Cases)
    # =========================================================================
    cases.append(
        EvaluationCase(
            case_id="A-01",
            category="confirmed_drift",
            name="stale_numeric_timeout_default",
            description="Default network timeout increased from 30 to 60 seconds; doc still states 30.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    return True\n",
                "docs/config.md": "# Config\nThe default timeout is 30 seconds.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    return True\n",
                "docs/config.md": "# Config\nThe default timeout is 30 seconds.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/config.md",
            rationale="Code defaults to 60, doc asserts 30 seconds without historical qualification.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-02",
            category="confirmed_drift",
            name="stale_string_host_default",
            description="Default server bind host changed from 'localhost' to '0.0.0.0'.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/server.py": "def serve(host='localhost', port=8000):\n    pass\n",
                "docs/server.md": "# Server\nBy default, host is set to localhost.\n",
            },
            files_head={
                "src/server.py": "def serve(host='0.0.0.0', port=8000):\n    pass\n",
                "docs/server.md": "# Server\nBy default, host is set to localhost.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/server.md",
            rationale="Default host literal changed to '0.0.0.0', doc claims localhost.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-03",
            category="confirmed_drift",
            name="removed_public_parameter",
            description="Parameter 'username' removed from login(); guide still instructs users to supply it.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/auth.py": "def login(username, password):\n    pass\n",
                "docs/auth.md": "# Auth\nSupply your `username` and password.\n",
            },
            files_head={
                "src/auth.py": "def login(email, password):\n    pass\n",
                "docs/auth.md": "# Auth\nSupply your `username` and password.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-PARAM-002",
            expected_doc_file="docs/auth.md",
            rationale="Removed parameter is explicitly referenced in documentation.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-04",
            category="confirmed_drift",
            name="removed_cache_dir_parameter",
            description="Parameter 'cache_dir' removed from setup_environment.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/env.py": "def setup_env(app_name, cache_dir='/tmp/cache'):\n    pass\n",
                "docs/setup.md": "# Setup\nSpecify `cache_dir` to customize directory.\n",
            },
            files_head={
                "src/env.py": "def setup_env(app_name):\n    pass\n",
                "docs/setup.md": "# Setup\nSpecify `cache_dir` to customize directory.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-PARAM-002",
            expected_doc_file="docs/setup.md",
            rationale="cache_dir parameter was deleted entirely.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-05",
            category="confirmed_drift",
            name="removed_public_function",
            description="Function old_connect() removed; quickstart still uses it.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/api.py": "def old_connect():\n    return True\n",
                "docs/quickstart.md": "# Quickstart\nCall `old_connect()` to initialize.\n",
            },
            files_head={
                "src/api.py": "def new_connect():\n    return True\n",
                "docs/quickstart.md": "# Quickstart\nCall `old_connect()` to initialize.\n",
            },
            expected_status="POTENTIAL_DRIFT",
            expected_rule_id="PY-SYMBOL-003",
            expected_doc_file="docs/quickstart.md",
            rationale="Symbol old_connect no longer exists in src/api.py.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-06",
            category="confirmed_drift",
            name="removed_public_class_helper",
            description="LegacySession helper class removed from session module.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/session.py": "class LegacySession:\n    pass\n",
                "docs/session.md": "# Session\nCreate instances of LegacySession.\n",
            },
            files_head={
                "src/session.py": "class UnifiedSession:\n    pass\n",
                "docs/session.md": "# Session\nCreate instances of LegacySession.\n",
            },
            expected_status="POTENTIAL_DRIFT",
            expected_rule_id="PY-SYMBOL-003",
            expected_doc_file="docs/session.md",
            rationale="LegacySession class deleted.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-07",
            category="confirmed_drift",
            name="cli_flag_removed",
            description="CLI flag '--verbose' removed from argparse parser.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/cli.py": "import argparse\np = argparse.ArgumentParser()\np.add_argument('--verbose')\n",
                "docs/cli.md": "# CLI\nPass `--verbose` to enable debug output.\n",
            },
            files_head={
                "src/cli.py": "import argparse\np = argparse.ArgumentParser()\np.add_argument('--log-level')\n",
                "docs/cli.md": "# CLI\nPass `--verbose` to enable debug output.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-CONFIG-004",
            expected_doc_file="docs/cli.md",
            rationale="--verbose was removed from CLI options.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-08",
            category="confirmed_drift",
            name="cli_flag_renamed",
            description="CLI flag '--timeout' renamed to '--request-timeout'.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/cli.py": "import argparse\np = argparse.ArgumentParser()\np.add_argument('--timeout')\n",
                "docs/cli.md": "# CLI Reference\n`--timeout`: Connection timeout.\n",
            },
            files_head={
                "src/cli.py": "import argparse\np = argparse.ArgumentParser()\np.add_argument('--request-timeout')\n",
                "docs/cli.md": "# CLI Reference\n`--timeout`: Connection timeout.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-CONFIG-004",
            expected_doc_file="docs/cli.md",
            rationale="--timeout is no longer recognized by the CLI.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-09",
            category="confirmed_drift",
            name="constant_max_connections_changed",
            description="Module constant MAX_CONNECTIONS changed from 10 to 25.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/settings.py": "MAX_CONNECTIONS = 10\n",
                "docs/settings.md": "# Settings\n`MAX_CONNECTIONS` defaults to 10.\n",
            },
            files_head={
                "src/settings.py": "MAX_CONNECTIONS = 25\n",
                "docs/settings.md": "# Settings\n`MAX_CONNECTIONS` defaults to 10.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-CONST-005",
            expected_doc_file="docs/settings.md",
            rationale="MAX_CONNECTIONS value updated in code, stale in docs.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-10",
            category="confirmed_drift",
            name="constant_default_port_changed",
            description="DEFAULT_PORT changed from 8080 to 9000.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/network.py": "DEFAULT_PORT = 8080\n",
                "docs/network.md": "# Network\nThe `DEFAULT_PORT` is set to 8080.\n",
            },
            files_head={
                "src/network.py": "DEFAULT_PORT = 9000\n",
                "docs/network.md": "# Network\nThe `DEFAULT_PORT` is set to 8080.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-CONST-005",
            expected_doc_file="docs/network.md",
            rationale="DEFAULT_PORT updated to 9000 in code.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-11",
            category="confirmed_drift",
            name="class_method_default_changed",
            description="Client.fetch() retries default updated from 3 to 5.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "class Client:\n    def fetch(self, retries=3):\n        pass\n",
                "docs/client.md": "# Client\nfetch() will attempt retries 3 times.\n",
            },
            files_head={
                "src/client.py": "class Client:\n    def fetch(self, retries=5):\n        pass\n",
                "docs/client.md": "# Client\nfetch() will attempt retries 3 times.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/client.md",
            rationale="Client.fetch method default updated in code.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-12",
            category="confirmed_drift",
            name="kwonly_arg_default_changed",
            description="Keyword-only parameter verify default changed from True to False.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/http.py": "def send(url, *, verify=True):\n    pass\n",
                "docs/http.md": "# HTTP\nBy default, `verify` is True.\n",
            },
            files_head={
                "src/http.py": "def send(url, *, verify=False):\n    pass\n",
                "docs/http.md": "# HTTP\nBy default, `verify` is True.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/http.md",
            rationale="Keyword-only default flipped from True to False.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-13",
            category="confirmed_drift",
            name="parameter_renamed_unaliased",
            description="Parameter 'query' renamed to 'q' without alias.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/search.py": "def search(query):\n    pass\n",
                "docs/search.md": "# Search\nPass `query` parameter as string.\n",
            },
            files_head={
                "src/search.py": "def search(q):\n    pass\n",
                "docs/search.md": "# Search\nPass `query` parameter as string.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-PARAM-002",
            expected_doc_file="docs/search.md",
            rationale="Old parameter 'query' removed.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="A-14",
            category="confirmed_drift",
            name="table_doc_stale_flag_default",
            description="Markdown table lists default timeout as 30; code changed to 60.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def request(timeout=30):\n    pass\n",
                "docs/params.md": "| Param | Default |\n| :--- | :--- |\n| `timeout` | 30 |\n",
            },
            files_head={
                "src/client.py": "def request(timeout=60):\n    pass\n",
                "docs/params.md": "| Param | Default |\n| :--- | :--- |\n| `timeout` | 30 |\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/params.md",
            rationale="Table cell still lists stale default 30.",
        )
    )

    # =========================================================================
    # CATEGORY B: Negative Controls (14 Cases)
    # =========================================================================
    cases.append(
        EvaluationCase(
            case_id="B-01",
            category="negative_control",
            name="internal_private_helper_renamed",
            description="Private helper _calc_hash renamed to _hash_buffer; public doc unchanged.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/crypto.py": "def _calc_hash(data):\n    return hash(data)\n\ndef encrypt(data):\n    return _calc_hash(data)\n",
                "docs/security.md": "# Security\nCall `encrypt(data)` to protect records.\n",
            },
            files_head={
                "src/crypto.py": "def _hash_buffer(data):\n    return hash(data)\n\ndef encrypt(data):\n    return _hash_buffer(data)\n",
                "docs/security.md": "# Security\nCall `encrypt(data)` to protect records.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Private helper change does not affect public documentation.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-02",
            category="negative_control",
            name="local_variable_rename",
            description="Local variable inside function body renamed for performance.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/calc.py": "def compute(a, b):\n    temp = a + b\n    return temp\n",
                "docs/calc.md": "# Calculator\n`compute(a, b)` returns sum of numbers.\n",
            },
            files_head={
                "src/calc.py": "def compute(a, b):\n    total = a + b\n    return total\n",
                "docs/calc.md": "# Calculator\n`compute(a, b)` returns sum of numbers.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Internal variable rename has no public API impact.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-03",
            category="negative_control",
            name="code_comment_only_changed",
            description="Comments modified in python file; AST signature and defaults identical.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/db.py": "# Old DB Comment\ndef query(sql, timeout=30):\n    return []\n",
                "docs/db.md": "# Database\n`query` takes `timeout` defaulting to 30.\n",
            },
            files_head={
                "src/db.py": "# Updated descriptive comment explaining query planner\ndef query(sql, timeout=30):\n    return []\n",
                "docs/db.md": "# Database\n`query` takes `timeout` defaulting to 30.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Comment modifications do not alter AST facts.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-04",
            category="negative_control",
            name="whitespace_formatting_only",
            description="File reformatted with Black; code AST identical.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/utils.py": "def clean(x,y=10):\n    return x*y\n",
                "docs/utils.md": "# Utils\n`clean` has `y` defaulting to 10.\n",
            },
            files_head={
                "src/utils.py": "def clean(x, y=10):\n    return x * y\n",
                "docs/utils.md": "# Utils\n`clean` has `y` defaulting to 10.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Formatting change only; AST normalized defaults identical.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-05",
            category="negative_control",
            name="unit_test_file_modified_only",
            description="Changes in tests/test_api.py; production source and docs untouched.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/api.py": "def ping():\n    return 'pong'\n",
                "tests/test_api.py": "def test_ping():\n    assert ping() == 'pong'\n",
                "docs/api.md": "# API\nCall `ping()` to check health.\n",
            },
            files_head={
                "src/api.py": "def ping():\n    return 'pong'\n",
                "tests/test_api.py": "def test_ping():\n    # Added extra assertion\n    assert ping() == 'pong'\n    assert True\n",
                "docs/api.md": "# API\nCall `ping()` to check health.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Test files are excluded or non-impacting on public API docs.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-06",
            category="negative_control",
            name="code_and_docs_synced_in_same_pr",
            description="Default changed from 30 to 60, and docs updated simultaneously to 60.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    pass\n",
                "docs/config.md": "# Config\nThe default timeout is 30 seconds.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    pass\n",
                "docs/config.md": "# Config\nThe default timeout is 60 seconds.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Documentation was correctly updated within the PR.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-07",
            category="negative_control",
            name="param_removed_and_docs_updated",
            description="Parameter 'username' removed from code and removed from docs in same PR.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/auth.py": "def login(username, password):\n    pass\n",
                "docs/auth.md": "# Auth\nPass `username` and password.\n",
            },
            files_head={
                "src/auth.py": "def login(email, password):\n    pass\n",
                "docs/auth.md": "# Auth\nPass `email` and password.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Documentation was kept in sync with parameter removal.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-08",
            category="negative_control",
            name="new_optional_parameter_added",
            description="New optional parameter limit=100 added; existing docs omit it without contradiction.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/query.py": "def query(sql, timeout=30):\n    pass\n",
                "docs/query.md": "# Query\n`query(sql, timeout=30)` executes a query.\n",
            },
            files_head={
                "src/query.py": "def query(sql, timeout=30, limit=100):\n    pass\n",
                "docs/query.md": "# Query\n`query(sql, timeout=30)` executes a query.\n",
            },
            expected_status="NO_DRIFT",
            acceptable_statuses=["POTENTIAL_DRIFT"],
            rationale="Adding an optional parameter with default does not break documented usage.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-09",
            category="negative_control",
            name="non_code_repo_file_added",
            description="Repository adds LICENSE or .gitignore without modifying Python code.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/app.py": "def run():\n    pass\n",
                "docs/run.md": "# Run\nCall `run()`.\n",
            },
            files_head={
                "src/app.py": "def run():\n    pass\n",
                "docs/run.md": "# Run\nCall `run()`.\n",
                "LICENSE": "MIT License\n",
            },
            expected_status="NO_DRIFT",
            rationale="No code changes occurred.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-10",
            category="negative_control",
            name="historical_comparison_in_docs",
            description="Doc explicitly compares: 'Previously the timeout was 30; now it is 60.'",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    pass\n",
                "docs/config.md": "# Config\nThe timeout is 30 seconds.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    pass\n",
                "docs/config.md": "# Config\nPreviously the timeout was 30; now it defaults to 60.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Document mentions old value in explicit historical comparison context.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-11",
            category="negative_control",
            name="formerly_labeled_default",
            description="Doc explicitly says: 'Formerly, timeout was 30 seconds.'",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    pass\n",
                "docs/config.md": "# Config\nThe timeout was 30 seconds.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    pass\n",
                "docs/config.md": "# Config\nFormerly, timeout was 30 seconds before version 2.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Historical qualifier suppresses false positive.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-12",
            category="negative_control",
            name="different_function_shares_value",
            description="cache(timeout=30) remains 30; connect(timeout=60) changed. Doc for cache is accurate.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    pass\n\ndef cache(timeout=30):\n    pass\n",
                "docs/cache.md": "# Cache\n`cache` timeout is 30 seconds.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    pass\n\ndef cache(timeout=30):\n    pass\n",
                "docs/cache.md": "# Cache\n`cache` timeout is 30 seconds.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Doc is linked to cache(), which did not change its default.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-13",
            category="negative_control",
            name="type_annotation_refactored_only",
            description="Parameter type hint refined from int to float; runtime default 30 unchanged.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/calc.py": "def scale(factor: int = 30):\n    pass\n",
                "docs/calc.md": "# Calc\n`scale` has default factor of 30.\n",
            },
            files_head={
                "src/calc.py": "def scale(factor: float = 30):\n    pass\n",
                "docs/calc.md": "# Calc\n`scale` has default factor of 30.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Literal default value is identical (30).",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="B-14",
            category="negative_control",
            name="docstring_internal_notes_updated",
            description="Private docstring modified; public markdown user guide unchanged.",
            difficulty="low",
            target_engine="deterministic",
            files_base={
                "src/worker.py": 'def process():\n    """Old docstring."""\n    pass\n',
                "docs/worker.md": "# Worker\nCall `process()` to start worker.\n",
            },
            files_head={
                "src/worker.py": 'def process():\n    """New developer architecture notes."""\n    pass\n',
                "docs/worker.md": "# Worker\nCall `process()` to start worker.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Docstring changes inside source code don't invalidate user documentation.",
        )
    )

    # =========================================================================
    # CATEGORY C: Ambiguous, Aliased & Difficult Cases (12 Cases)
    # =========================================================================
    cases.append(
        EvaluationCase(
            case_id="C-01",
            category="ambiguous_edge_case",
            name="function_renamed_with_compatibility_alias",
            description="Function renamed to new_connect(), but old_connect = new_connect alias exists.",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/client.py": "def old_connect():\n    return True\n",
                "docs/client.md": "# Client\nCall `old_connect()` to initialize.\n",
            },
            files_head={
                "src/client.py": "def new_connect():\n    return True\n\nold_connect = new_connect\n",
                "docs/client.md": "# Client\nCall `old_connect()` to initialize.\n",
            },
            expected_status="NO_DRIFT",
            acceptable_statuses=["POTENTIAL_DRIFT", "UNCERTAIN"],
            rationale="Compatibility alias preserves public function availability.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-02",
            category="ambiguous_edge_case",
            name="symbol_reexported_in_all",
            description="Symbol re-exported in __all__; internal implementation moved.",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/__init__.py": "__all__ = ['run']\ndef run():\n    pass\n",
                "docs/init.md": "# Init\nCall `run()` from package root.\n",
            },
            files_head={
                "src/__init__.py": "from .core import run\n__all__ = ['run']\n",
                "src/core.py": "def run():\n    pass\n",
                "docs/init.md": "# Init\nCall `run()` from package root.\n",
            },
            expected_status="NO_DRIFT",
            acceptable_statuses=["UNCERTAIN"],
            rationale="Symbol is still exposed at package level.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-03",
            category="ambiguous_edge_case",
            name="typing_overload_declarations",
            description="typing.overload declarations alongside implementation.",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/over.py": "from typing import overload\n@overload\ndef get(x: int) -> int: ...\n@overload\ndef get(x: str) -> str: ...\ndef get(x):\n    return x\n",
                "docs/over.md": "# Overload\n`get(x)` returns x.\n",
            },
            files_head={
                "src/over.py": "from typing import overload\n@overload\ndef get(x: int) -> int: ...\n@overload\ndef get(x: str) -> str: ...\n@overload\ndef get(x: float) -> float: ...\ndef get(x):\n    return x\n",
                "docs/over.md": "# Overload\n`get(x)` returns x.\n",
            },
            expected_status="NO_DRIFT",
            acceptable_statuses=["UNCERTAIN"],
            rationale="Adding a type overload declaration does not break existing documentation.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-04",
            category="ambiguous_edge_case",
            name="dynamic_default_via_constant",
            description="Function default references module constant; constant value changed.",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/cfg.py": "DEFAULT_T = 30\ndef send(timeout=DEFAULT_T):\n    pass\n",
                "docs/cfg.md": "# Config\n`send` timeout defaults to 30.\n",
            },
            files_head={
                "src/cfg.py": "DEFAULT_T = 60\ndef send(timeout=DEFAULT_T):\n    pass\n",
                "docs/cfg.md": "# Config\n`send` timeout defaults to 30.\n",
            },
            expected_status="DRIFT",
            acceptable_statuses=["POTENTIAL_DRIFT"],
            expected_rule_id="PY-CONST-005",
            rationale="DEFAULT_T changed from 30 to 60, making doc stale.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-05",
            category="ambiguous_edge_case",
            name="env_var_default_resolution",
            description="Default loaded dynamically via os.getenv('PORT', 8000).",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/net.py": "import os\ndef serve(port=int(os.getenv('PORT', 8000))):\n    pass\n",
                "docs/net.md": "# Network\nDefault port is 8000.\n",
            },
            files_head={
                "src/net.py": "import os\ndef serve(port=int(os.getenv('PORT', 9000))):\n    pass\n",
                "docs/net.md": "# Network\nDefault port is 8000.\n",
            },
            expected_status="UNCERTAIN",
            acceptable_statuses=["DRIFT", "POTENTIAL_DRIFT"],
            rationale="Dynamic expression default requires conservative evaluation or AI interpretation.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-06",
            category="ambiguous_edge_case",
            name="subclass_override_without_sig_change",
            description="Child class overrides method without modifying parameters or defaults.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/base.py": "class Base:\n    def execute(self, timeout=30):\n        return 1\n",
                "docs/base.md": "# Base\n`execute` defaults to timeout 30.\n",
            },
            files_head={
                "src/base.py": "class Base:\n    def execute(self, timeout=30):\n        return 1\nclass Child(Base):\n    def execute(self, timeout=30):\n        return 2\n",
                "docs/base.md": "# Base\n`execute` defaults to timeout 30.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Subclass implementation preserves base signature and defaults.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-07",
            category="ambiguous_edge_case",
            name="dynamic_dispatch_getattr",
            description="Function calls routed through getattr; ambiguous static signals.",
            difficulty="adversarial",
            target_engine="ai_assisted",
            files_base={
                "src/dispatch.py": "def handle(cmd):\n    fn = getattr(commands, cmd)\n    return fn()\n",
                "docs/cmd.md": "# Commands\nAvailable command: `ping`.\n",
            },
            files_head={
                "src/dispatch.py": "def handle(cmd):\n    fn = getattr(commands, f'do_{cmd}')\n    return fn()\n",
                "docs/cmd.md": "# Commands\nAvailable command: `ping`.\n",
            },
            expected_status="UNCERTAIN",
            acceptable_statuses=["POTENTIAL_DRIFT", "NO_DRIFT"],
            rationale="Dynamic dispatch string manipulation cannot be proven false statically.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-08",
            category="ambiguous_edge_case",
            name="conditional_default_in_body",
            description="Signature has timeout=None; default resolved inside function body.",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/body.py": "def fetch(timeout=None):\n    if timeout is None:\n        timeout = 30\n    return timeout\n",
                "docs/body.md": "# Fetch\nDefault timeout is 30.\n",
            },
            files_head={
                "src/body.py": "def fetch(timeout=None):\n    if timeout is None:\n        timeout = 60\n    return timeout\n",
                "docs/body.md": "# Fetch\nDefault timeout is 30.\n",
            },
            expected_status="UNCERTAIN",
            acceptable_statuses=["POTENTIAL_DRIFT", "DRIFT"],
            rationale="AST signature has timeout=None; body modification requires semantic interpretation.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-09",
            category="ambiguous_edge_case",
            name="decorator_modifies_behavior",
            description="Decorator added to function altering retry count.",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/retry.py": "def call():\n    pass\n",
                "docs/retry.md": "# Retry\n`call` executes once.\n",
            },
            files_head={
                "src/retry.py": "@retry(attempts=3)\ndef call():\n    pass\n",
                "docs/retry.md": "# Retry\n`call` executes once.\n",
            },
            expected_status="UNCERTAIN",
            acceptable_statuses=["POTENTIAL_DRIFT"],
            rationale="Decorator semantics require behavioral interpretation.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-10",
            category="ambiguous_edge_case",
            name="same_function_name_in_two_modules",
            description="auth.login and admin.login exist; admin.login changed timeout, auth doc intact.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/auth.py": "def login(timeout=30):\n    pass\n",
                "src/admin.py": "def login(timeout=30):\n    pass\n",
                "docs/auth.md": "# Auth\nauth.login uses timeout of 30.\n",
            },
            files_head={
                "src/auth.py": "def login(timeout=30):\n    pass\n",
                "src/admin.py": "def login(timeout=60):\n    pass\n",
                "docs/auth.md": "# Auth\nauth.login uses timeout of 30.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Only admin.login changed; auth.md correctly references auth.login.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-11",
            category="ambiguous_edge_case",
            name="variadic_kwargs_forwarding",
            description="Function accepts **kwargs forwarding to internal helper.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/proxy.py": "def proxy(**kwargs):\n    pass\n",
                "docs/proxy.md": "# Proxy\nAccepts arbitrary options.\n",
            },
            files_head={
                "src/proxy.py": "def proxy(mode='fast', **kwargs):\n    pass\n",
                "docs/proxy.md": "# Proxy\nAccepts arbitrary options.\n",
            },
            expected_status="NO_DRIFT",
            acceptable_statuses=["POTENTIAL_DRIFT"],
            rationale="Adding a named option with default does not break arbitrary kwargs.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="C-12",
            category="ambiguous_edge_case",
            name="runtime_deprecation_warning",
            description="Function emits DeprecationWarning when called.",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/dep.py": "def legacy_call():\n    return 1\n",
                "docs/dep.md": "# Legacy\nCall `legacy_call()`.\n",
            },
            files_head={
                "src/dep.py": "import warnings\ndef legacy_call():\n    warnings.warn('deprecated', DeprecationWarning)\n    return 1\n",
                "docs/dep.md": "# Legacy\nCall `legacy_call()`.\n",
            },
            expected_status="UNCERTAIN",
            acceptable_statuses=["NO_DRIFT", "POTENTIAL_DRIFT"],
            rationale="Function is still callable; deprecation is a semantic warning.",
        )
    )

    # =========================================================================
    # CATEGORY D: Documentation Semantics & Formatting (10 Cases)
    # =========================================================================
    cases.append(
        EvaluationCase(
            case_id="D-01",
            category="doc_semantics",
            name="migration_guide_v1_to_v2",
            description="Migration guide documents breaking change: 'In v1, timeout was 30; in v2 it is 60.'",
            difficulty="high",
            target_engine="both",
            files_base={
                "src/conn.py": "def connect(timeout=30):\n    pass\n",
                "docs/migration.md": "# Migration\nUpgrade guide.\n",
            },
            files_head={
                "src/conn.py": "def connect(timeout=60):\n    pass\n",
                "docs/migration.md": "# Migration\nIn version 1, timeout was 30; in version 2 it defaults to 60.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Migration guide explicitly documents both versions without stale claims.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-02",
            category="doc_semantics",
            name="changelog_file_release_notes",
            description="CHANGELOG.md contains release notes mentioning previous default 30.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/app.py": "def run(timeout=30):\n    pass\n",
                "CHANGELOG.md": "# Changelog\n## v1.0.0\n- Initial release with timeout=30\n",
            },
            files_head={
                "src/app.py": "def run(timeout=60):\n    pass\n",
                "CHANGELOG.md": "# Changelog\n## v2.0.0\n- Bump timeout to 60\n## v1.0.0\n- Initial release with timeout=30\n",
            },
            expected_status="NO_DRIFT",
            rationale="Changelogs are historical by definition.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-03",
            category="doc_semantics",
            name="fenced_code_pseudocode_example",
            description="Fenced code block shows pseudo-code with custom timeout; code default changed to 60.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    pass\n",
                "docs/example.md": "# Example\n```python\n# User custom timeout\nclient.connect(timeout=999)\n```\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    pass\n",
                "docs/example.md": "# Example\n```python\n# User custom timeout\nclient.connect(timeout=999)\n```\n",
            },
            expected_status="NO_DRIFT",
            rationale="Example demonstrates passing an explicit custom value (999), not asserting a default.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-04",
            category="doc_semantics",
            name="multiple_doc_occurrences_one_stale",
            description="Doc has two sections: Section 1 correctly updated to 60, Section 2 overlooked still saying 30.",
            difficulty="high",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    pass\n",
                "docs/guide.md": "## Overview\nThe default timeout is 30 seconds.\n\n## Advanced\nThe timeout parameter defaults to 30.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    pass\n",
                "docs/guide.md": "## Overview\nThe default timeout is 60 seconds.\n\n## Advanced\nThe timeout parameter defaults to 30.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/guide.md",
            rationale="Advanced section still contains stale default 30.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-05",
            category="doc_semantics",
            name="deeply_nested_headings_context",
            description="Doc has H1 > H2 > H3 > H4 hierarchy.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/network.py": "def connect(timeout=30):\n    pass\n",
                "docs/deep.md": "# Core\n## Network\n### Client\n#### Sockets\nThe default timeout is 30 seconds.\n",
            },
            files_head={
                "src/network.py": "def connect(timeout=60):\n    pass\n",
                "docs/deep.md": "# Core\n## Network\n### Client\n#### Sockets\nThe default timeout is 30 seconds.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/deep.md",
            rationale="DocSpan must preserve full heading stack ['Core', 'Network', 'Client', 'Sockets'].",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-06",
            category="doc_semantics",
            name="multi_column_table_defaults",
            description="Markdown table with multiple columns: Parameter, Type, Default, Description.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def fetch(host='localhost', timeout=30, retries=3):\n    pass\n",
                "docs/table.md": "| Param | Type | Default | Description |\n| :--- | :--- | :--- | :--- |\n| `timeout` | int | 30 | Timeout in seconds |\n| `retries` | int | 3 | Retry count |\n",
            },
            files_head={
                "src/client.py": "def fetch(host='localhost', timeout=60, retries=3):\n    pass\n",
                "docs/table.md": "| Param | Type | Default | Description |\n| :--- | :--- | :--- | :--- |\n| `timeout` | int | 30 | Timeout in seconds |\n| `retries` | int | 3 | Retry count |\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/table.md",
            rationale="Table cell for timeout default is stale.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-07",
            category="doc_semantics",
            name="unrelated_number_in_prose",
            description="Doc mentions '30 connections per worker'; code changed timeout from 10 to 20.",
            difficulty="adversarial",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=10):\n    pass\n",
                "docs/client.md": "# Client\nSupports 30 concurrent worker connections.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=20):\n    pass\n",
                "docs/client.md": "# Client\nSupports 30 concurrent worker connections.\n",
            },
            expected_status="NO_DRIFT",
            rationale="Number 30 refers to concurrent connections, not timeout.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-08",
            category="doc_semantics",
            name="multi_sentence_paragraph_stale_second_sentence",
            description="Paragraph has 3 sentences; only second sentence has stale default.",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/client.py": "def connect(timeout=30):\n    pass\n",
                "docs/guide.md": "Fast HTTP client. The default timeout is 30 seconds. Works on Python 3.12.\n",
            },
            files_head={
                "src/client.py": "def connect(timeout=60):\n    pass\n",
                "docs/guide.md": "Fast HTTP client. The default timeout is 30 seconds. Works on Python 3.12.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-DEFAULT-001",
            expected_doc_file="docs/guide.md",
            rationale="Sentence-level splitting should isolate 'The default timeout is 30 seconds.'",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-09",
            category="doc_semantics",
            name="inline_formatted_backticks_and_links",
            description="Flag formatted as markdown link [`--timeout`](https://example.com/flags).",
            difficulty="medium",
            target_engine="deterministic",
            files_base={
                "src/cli.py": "import argparse\np = argparse.ArgumentParser()\np.add_argument('--timeout')\n",
                "docs/flags.md": "# Flags\nSee [`--timeout`](https://example.com/flags) for details.\n",
            },
            files_head={
                "src/cli.py": "import argparse\np = argparse.ArgumentParser()\np.add_argument('--request-timeout')\n",
                "docs/flags.md": "# Flags\nSee [`--timeout`](https://example.com/flags) for details.\n",
            },
            expected_status="DRIFT",
            expected_rule_id="PY-CONFIG-004",
            expected_doc_file="docs/flags.md",
            rationale="--timeout flag is removed even if wrapped in a markdown link.",
        )
    )

    cases.append(
        EvaluationCase(
            case_id="D-10",
            category="doc_semantics",
            name="external_url_containing_symbol_name",
            description="URL has /api/connect in href; function connect(timeout=30) unchanged.",
            difficulty="adversarial",
            target_engine="deterministic",
            files_base={
                "src/net.py": "def connect(timeout=30):\n    pass\n",
                "docs/links.md": "# Links\nVisit [GitHub Connect](https://example.com/api/connect) for status.\n",
            },
            files_head={
                "src/net.py": "def connect(timeout=30):\n    pass\n",
                "docs/links.md": "# Links\nVisit [GitHub Connect](https://example.com/api/connect) for status.\n",
            },
            expected_status="NO_DRIFT",
            rationale="No changes to connect; URL mention does not create false drift.",
        )
    )

    return cases
