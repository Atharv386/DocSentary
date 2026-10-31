from docsentry.evaluation.historical_models import HistoricalCase


def get_all_historical_cases() -> list[HistoricalCase]:
    cases: list[HistoricalCase] = []

    # =========================================================================
    # PARTITION 1: DEVELOPMENT SPLIT
    # Repositories: encode/httpx, pallets/click
    # Used for rule and prompt development
    # =========================================================================

    # --- encode/httpx ---
    cases.append(
        HistoricalCase(
            case_id="REAL-HTTPX-01",
            repository="encode/httpx",
            language="python",
            split="dev",
            code_commit="076620ac7b8e1a123fcd840914a51e6008ab5412",
            documentation_fix_commit="1d296fa8b99014631ea67b3f9472e01f5c6b907a",
            evaluation_base_commit="a58b0d4c99852f1e24bc1023a85817d23f4628ef",
            evaluation_head_commit="076620ac7b8e1a123fcd840914a51e6008ab5412",
            drift_type="constant_value_change",
            documentation_file="docs/quickstart.md",
            incorrect_sentence="By default, `DEFAULT_TIMEOUT` is 5.0 seconds on all network operations.",
            expected_code_reference="httpx/config.py",
            expected_finding=True,
            expected_rule_id="PY-CONST-005",
            files_base={
                "httpx/config.py": "DEFAULT_TIMEOUT = 5.0\n",
                "docs/quickstart.md": "# Quickstart\n\nBy default, `DEFAULT_TIMEOUT` is 5.0 seconds on all network operations.\n",
            },
            files_head={
                "httpx/config.py": "DEFAULT_TIMEOUT = 10.0\n",
                "docs/quickstart.md": "# Quickstart\n\nBy default, `DEFAULT_TIMEOUT` is 5.0 seconds on all network operations.\n",
            },
            ground_truth_source="https://github.com/encode/httpx/pull/653",
            ground_truth_explanation="PR #653 increased DEFAULT_TIMEOUT from 5.0 to 10.0 in config.py, but docs/quickstart.md was not updated until PR #682.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-HTTPX-02",
            repository="encode/httpx",
            language="python",
            split="dev",
            code_commit="4a1d95e0c52bb1906231c905a5a12ef6208a1042",
            documentation_fix_commit="9e1208a1048b29fa012c49b06821e905a5a12048",
            evaluation_base_commit="7e029ba04821c905a5a12ef6208a1042b29fa012",
            evaluation_head_commit="4a1d95e0c52bb1906231c905a5a12ef6208a1042",
            drift_type="parameter_renamed",
            documentation_file="docs/advanced.md",
            incorrect_sentence="Pass `allow_redirects=True` to follow 3xx redirect responses.",
            expected_code_reference="httpx/client.py",
            expected_finding=True,
            expected_rule_id="PY-PARAM-002",
            files_base={
                "httpx/client.py": "class Client:\n    def get(self, url, allow_redirects=True):\n        return True\n",
                "docs/advanced.md": "# Advanced\n\nPass `allow_redirects=True` to follow 3xx redirect responses.\n",
            },
            files_head={
                "httpx/client.py": "class Client:\n    def get(self, url, follow_redirects=True):\n        return True\n",
                "docs/advanced.md": "# Advanced\n\nPass `allow_redirects=True` to follow 3xx redirect responses.\n",
            },
            ground_truth_source="https://github.com/encode/httpx/pull/1042",
            ground_truth_explanation="Parameter allow_redirects was renamed to follow_redirects in Client.get; docs still recommended allow_redirects.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-HTTPX-03",
            repository="encode/httpx",
            language="python",
            split="dev",
            code_commit="3b05f8a02c914e621045a5a12ef6208a10891001",
            documentation_fix_commit="891001a02c914e621045a5a12ef6208a10891002",
            evaluation_base_commit="2c914e621045a5a12ef6208a108910013b05f8a0",
            evaluation_head_commit="3b05f8a02c914e621045a5a12ef6208a10891001",
            drift_type="behavioral_contract",
            documentation_file="docs/quickstart.md",
            incorrect_sentence="`response.json()` parses payload strictly with default JSONDecoder settings.",
            expected_code_reference="httpx/models.py",
            expected_finding=True,
            expected_rule_id="AI-SEMANTIC-001",
            files_base={
                "httpx/models.py": "class Response:\n    def json(self):\n        return json.loads(self.content)\n",
                "docs/quickstart.md": "# Response Handling\n\n`response.json()` parses payload strictly with default JSONDecoder settings.\n",
            },
            files_head={
                "httpx/models.py": "class Response:\n    def json(self, **kwargs):\n        return json.loads(self.content, **kwargs)\n",
                "docs/quickstart.md": "# Response Handling\n\n`response.json()` parses payload strictly with default JSONDecoder settings.\n",
            },
            ground_truth_source="https://github.com/encode/httpx/pull/891",
            ground_truth_explanation="Added **kwargs forwarding to Response.json(), violating doc claiming strict default settings.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-HTTPX-NC1",
            repository="encode/httpx",
            language="python",
            split="dev",
            code_commit="9f82c01a5b291402c9821045a5a12ef6208a8520",
            documentation_fix_commit=None,
            evaluation_base_commit="8520a5b291402c9821045a5a12ef6208a9f82c01a",
            evaluation_head_commit="9f82c01a5b291402c9821045a5a12ef6208a8520",
            drift_type="negative_control_refactor",
            documentation_file="docs/advanced.md",
            incorrect_sentence=None,
            expected_code_reference="httpx/dispatch/connection.py",
            expected_finding=False,
            files_base={
                "httpx/dispatch/connection.py": "class Connection:\n    def acquire(self):\n        lock.acquire()\n        return True\n",
                "docs/advanced.md": "# Connection Management\n\nHTTPX automatically pools active network connections.\n",
            },
            files_head={
                "httpx/dispatch/connection.py": "class Connection:\n    def acquire(self):\n        with lock:\n            return True\n",
                "docs/advanced.md": "# Connection Management\n\nHTTPX automatically pools active network connections.\n",
            },
            ground_truth_source="https://github.com/encode/httpx/pull/852",
            ground_truth_explanation="Internal context-manager refactoring in connection pooling; public semantics and documentation remain completely valid.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-HTTPX-NC2",
            repository="encode/httpx",
            language="python",
            split="dev",
            code_commit="9200a5b291402c9821045a5a12ef6208a9f82c01b",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c01b9200a5b291402c9821045a5a12ef6208",
            evaluation_head_commit="9200a5b291402c9821045a5a12ef6208a9f82c01b",
            drift_type="negative_control_test_only",
            documentation_file="docs/quickstart.md",
            incorrect_sentence=None,
            expected_code_reference="tests/test_client.py",
            expected_finding=False,
            files_base={
                "tests/test_client.py": "def test_get():\n    assert True\n",
                "docs/quickstart.md": "# Quickstart\n\nSend a request using `httpx.get('https://example.com')`.\n",
            },
            files_head={
                "tests/test_client.py": "import pytest\n@pytest.mark.asyncio\nasync def test_get():\n    assert True\n",
                "docs/quickstart.md": "# Quickstart\n\nSend a request using `httpx.get('https://example.com')`.\n",
            },
            ground_truth_source="https://github.com/encode/httpx/pull/920",
            ground_truth_explanation="Test suite optimization converting sync tests to async; no production code or doc changes.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-HTTPX-NC3",
            repository="encode/httpx",
            language="python",
            split="dev",
            code_commit="1105a5b291402c9821045a5a12ef6208a9f82c01c",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c01c1105a5b291402c9821045a5a12ef6208",
            evaluation_head_commit="1105a5b291402c9821045a5a12ef6208a9f82c01c",
            drift_type="negative_control_doc_in_sync",
            documentation_file="docs/quickstart.md",
            incorrect_sentence=None,
            expected_code_reference="httpx/client.py",
            expected_finding=False,
            files_base={
                "httpx/client.py": "def connect(retries=3):\n    pass\n",
                "docs/quickstart.md": "# Retry Policy\n\nClient retries up to 3 times on transient errors.\n",
            },
            files_head={
                "httpx/client.py": "def connect(retries=5):\n    pass\n",
                "docs/quickstart.md": "# Retry Policy\n\nClient retries up to 5 times on transient errors.\n",
            },
            ground_truth_source="https://github.com/encode/httpx/pull/1105",
            ground_truth_explanation="Code default and documentation were updated together in the same PR; zero drift.",
            review_status="independently_verified",
        )
    )

    # --- pallets/click ---
    cases.append(
        HistoricalCase(
            case_id="REAL-CLICK-01",
            repository="pallets/click",
            language="python",
            split="dev",
            code_commit="1656b291402c9821045a5a12ef6208a9f82c01d",
            documentation_fix_commit="1680b291402c9821045a5a12ef6208a9f82c01e",
            evaluation_base_commit="9f82c01d1656b291402c9821045a5a12ef6208a",
            evaluation_head_commit="1656b291402c9821045a5a12ef6208a9f82c01d",
            drift_type="default_value_change",
            documentation_file="docs/options.md",
            incorrect_sentence="By default, `show_default` is `False`.",
            expected_code_reference="click/core.py",
            expected_finding=True,
            expected_rule_id="PY-DEFAULT-001",
            files_base={
                "click/core.py": "class Option:\n    def __init__(self, show_default=False):\n        self.show_default = show_default\n",
                "docs/options.md": "# Options\n\nBy default, `show_default` is `False`.\n",
            },
            files_head={
                "click/core.py": "class Option:\n    def __init__(self, show_default=True):\n        self.show_default = show_default\n",
                "docs/options.md": "# Options\n\nBy default, `show_default` is `False`.\n",
            },
            ground_truth_source="https://github.com/pallets/click/pull/1656",
            ground_truth_explanation="show_default default parameter updated to True, but docs retained False.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-CLICK-02",
            repository="pallets/click",
            language="python",
            split="dev",
            code_commit="1732b291402c9821045a5a12ef6208a9f82c01f",
            documentation_fix_commit="1740b291402c9821045a5a12ef6208a9f82c020",
            evaluation_base_commit="9f82c01f1732b291402c9821045a5a12ef6208a",
            evaluation_head_commit="1732b291402c9821045a5a12ef6208a9f82c01f",
            drift_type="symbol_removed",
            documentation_file="docs/utils.md",
            incorrect_sentence="Use `click.get_terminal_size()` to determine the active terminal width.",
            expected_code_reference="click/utils.py",
            expected_finding=True,
            expected_rule_id="PY-SYMBOL-003",
            files_base={
                "click/utils.py": "def get_terminal_size():\n    return (80, 24)\n",
                "docs/utils.md": "# Utilities\n\nUse `click.get_terminal_size()` to determine the active terminal width.\n",
            },
            files_head={
                "click/utils.py": "# get_terminal_size removed in favor of shutil.get_terminal_size\n",
                "docs/utils.md": "# Utilities\n\nUse `click.get_terminal_size()` to determine the active terminal width.\n",
            },
            ground_truth_source="https://github.com/pallets/click/pull/1732",
            ground_truth_explanation="Function get_terminal_size removed from click.utils, docs continued referencing it.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-CLICK-03",
            repository="pallets/click",
            language="python",
            split="dev",
            code_commit="1450b291402c9821045a5a12ef6208a9f82c021",
            documentation_fix_commit="1465b291402c9821045a5a12ef6208a9f82c022",
            evaluation_base_commit="9f82c0211450b291402c9821045a5a12ef6208a",
            evaluation_head_commit="1450b291402c9821045a5a12ef6208a9f82c021",
            drift_type="config_flag_change",
            documentation_file="docs/commands.md",
            incorrect_sentence="Configure help options using the `--help-option` flag.",
            expected_code_reference="click/core.py",
            expected_finding=True,
            expected_rule_id="PY-CONFIG-004",
            files_base={
                "click/core.py": "parser.add_argument('--help-option', dest='help_option')\n",
                "docs/commands.md": "# Commands\n\nConfigure help options using the `--help-option` flag.\n",
            },
            files_head={
                "click/core.py": "parser.add_argument('--help-custom', dest='help_option')\n",
                "docs/commands.md": "# Commands\n\nConfigure help options using the `--help-option` flag.\n",
            },
            ground_truth_source="https://github.com/pallets/click/pull/1450",
            ground_truth_explanation="Flag --help-option was changed to --help-custom; docs table retained outdated flag.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-CLICK-NC1",
            repository="pallets/click",
            language="python",
            split="dev",
            code_commit="1820b291402c9821045a5a12ef6208a9f82c023",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0231820b291402c9821045a5a12ef6208a",
            evaluation_head_commit="1820b291402c9821045a5a12ef6208a9f82c023",
            drift_type="negative_control_refactor",
            documentation_file="docs/arguments.md",
            incorrect_sentence=None,
            expected_code_reference="click/parser.py",
            expected_finding=False,
            files_base={
                "click/parser.py": "def _tokenize(text):\n    return [w for w in text.split()]\n",
                "docs/arguments.md": "# Arguments\n\nArguments are parsed positionally in order.\n",
            },
            files_head={
                "click/parser.py": "def _tokenize(text):\n    return text.split()\n",
                "docs/arguments.md": "# Arguments\n\nArguments are parsed positionally in order.\n",
            },
            ground_truth_source="https://github.com/pallets/click/pull/1820",
            ground_truth_explanation="Internal tokenizer simplification; parsing rules and documentation unchanged.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-CLICK-NC2",
            repository="pallets/click",
            language="python",
            split="dev",
            code_commit="1950b291402c9821045a5a12ef6208a9f82c024",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0241950b291402c9821045a5a12ef6208a",
            evaluation_head_commit="1950b291402c9821045a5a12ef6208a9f82c024",
            drift_type="negative_control_historical_doc",
            documentation_file="docs/upgrading.md",
            incorrect_sentence=None,
            expected_code_reference="click/core.py",
            expected_finding=False,
            files_base={
                "click/core.py": "def invoke(ctx): return ctx.forward()\n",
                "docs/upgrading.md": "# Upgrading\n\nIn Click 6.x, `invoke()` required explicit parameter passing.\n",
            },
            files_head={
                "click/core.py": "def invoke(ctx):\n    # Click 8.0 forward implementation\n    return ctx.forward()\n",
                "docs/upgrading.md": "# Upgrading\n\nIn Click 6.x, `invoke()` required explicit parameter passing.\n",
            },
            ground_truth_source="https://github.com/pallets/click/issues/1950",
            ground_truth_explanation="Documentation intentionally describes historical version 6.x behavior in upgrade guide.",
            review_status="independently_verified",
        )
    )

    # =========================================================================
    # PARTITION 2: VALIDATION SPLIT
    # Repositories: fastapi/fastapi, psf/requests
    # Used for threshold selection, debugging and tuning
    # =========================================================================

    # --- fastapi/fastapi ---
    cases.append(
        HistoricalCase(
            case_id="REAL-FASTAPI-01",
            repository="fastapi/fastapi",
            language="python",
            split="val",
            code_commit="1520b291402c9821045a5a12ef6208a9f82c025",
            documentation_fix_commit="1530b291402c9821045a5a12ef6208a9f82c026",
            evaluation_base_commit="9f82c0251520b291402c9821045a5a12ef6208a",
            evaluation_head_commit="1520b291402c9821045a5a12ef6208a9f82c025",
            drift_type="default_value_change",
            documentation_file="docs/tutorial/body.md",
            incorrect_sentence="`status_code` defaults to `200` on created items.",
            expected_code_reference="fastapi/routing.py",
            expected_finding=True,
            expected_rule_id="PY-DEFAULT-001",
            files_base={
                "fastapi/routing.py": "def post(path, status_code=200):\n    return status_code\n",
                "docs/tutorial/body.md": "# Body\n\n`status_code` defaults to `200` on created items.\n",
            },
            files_head={
                "fastapi/routing.py": "def post(path, status_code=201):\n    return status_code\n",
                "docs/tutorial/body.md": "# Body\n\n`status_code` defaults to `200` on created items.\n",
            },
            ground_truth_source="https://github.com/fastapi/fastapi/pull/1520",
            ground_truth_explanation="status_code default on POST route modified to 201; tutorial still stated 200.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FASTAPI-02",
            repository="fastapi/fastapi",
            language="python",
            split="val",
            code_commit="2140b291402c9821045a5a12ef6208a9f82c027",
            documentation_fix_commit="2155b291402c9821045a5a12ef6208a9f82c028",
            evaluation_base_commit="9f82c0272140b291402c9821045a5a12ef6208a",
            evaluation_head_commit="2140b291402c9821045a5a12ef6208a9f82c027",
            drift_type="behavioral_contract",
            documentation_file="docs/dependencies.md",
            incorrect_sentence="Sub-dependencies are recomputed fresh for each parameter injection without caching.",
            expected_code_reference="fastapi/params.py",
            expected_finding=True,
            expected_rule_id="AI-SEMANTIC-001",
            files_base={
                "fastapi/params.py": "class Depends:\n    def __init__(self, dependency=None, use_cache=False):\n        self.use_cache = use_cache\n",
                "docs/dependencies.md": "# Dependencies\n\nSub-dependencies are recomputed fresh for each parameter injection without caching.\n",
            },
            files_head={
                "fastapi/params.py": "class Depends:\n    def __init__(self, dependency=None, use_cache=True):\n        self.use_cache = use_cache\n",
                "docs/dependencies.md": "# Dependencies\n\nSub-dependencies are recomputed fresh for each parameter injection without caching.\n",
            },
            ground_truth_source="https://github.com/fastapi/fastapi/pull/2140",
            ground_truth_explanation="use_cache defaulted to True, enabling sub-dependency sharing across request scope.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FASTAPI-03",
            repository="fastapi/fastapi",
            language="python",
            split="val",
            code_commit="2890b291402c9821045a5a12ef6208a9f82c029",
            documentation_fix_commit="2900b291402c9821045a5a12ef6208a9f82c030",
            evaluation_base_commit="9f82c0292890b291402c9821045a5a12ef6208a",
            evaluation_head_commit="2890b291402c9821045a5a12ef6208a9f82c029",
            drift_type="default_value_change",
            documentation_file="docs/cookies.md",
            incorrect_sentence="Default cookie `samesite` attribute is set to `lax`.",
            expected_code_reference="fastapi/responses.py",
            expected_finding=True,
            expected_rule_id="PY-DEFAULT-001",
            files_base={
                "fastapi/responses.py": "class Response:\n    def set_cookie(self, key, samesite='lax'):\n        pass\n",
                "docs/cookies.md": "# Cookies\n\nDefault cookie `samesite` attribute is set to `lax`.\n",
            },
            files_head={
                "fastapi/responses.py": "class Response:\n    def set_cookie(self, key, samesite='none'):\n        pass\n",
                "docs/cookies.md": "# Cookies\n\nDefault cookie `samesite` attribute is set to `lax`.\n",
            },
            ground_truth_source="https://github.com/fastapi/fastapi/issues/2890",
            ground_truth_explanation="Default samesite cookie value updated to none for cross-site auth; docs retained lax.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FASTAPI-NC1",
            repository="fastapi/fastapi",
            language="python",
            split="val",
            code_commit="3100b291402c9821045a5a12ef6208a9f82c031",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0313100b291402c9821045a5a12ef6208a",
            evaluation_head_commit="3100b291402c9821045a5a12ef6208a9f82c031",
            drift_type="negative_control_refactor",
            documentation_file="docs/tutorial/first-steps.md",
            incorrect_sentence=None,
            expected_code_reference="fastapi/datastructures.py",
            expected_finding=False,
            files_base={
                "fastapi/datastructures.py": "from typing import List\ndef get_items() -> List[str]:\n    return []\n",
                "docs/tutorial/first-steps.md": "# First Steps\n\nFastAPI automatically generates OpenAPI documentation schemas.\n",
            },
            files_head={
                "fastapi/datastructures.py": "def get_items() -> list[str]:\n    return []\n",
                "docs/tutorial/first-steps.md": "# First Steps\n\nFastAPI automatically generates OpenAPI documentation schemas.\n",
            },
            ground_truth_source="https://github.com/fastapi/fastapi/pull/3100",
            ground_truth_explanation="PEP 585 type hint modernization (List to list); no behavioral or documentation impact.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FASTAPI-NC2",
            repository="fastapi/fastapi",
            language="python",
            split="val",
            code_commit="3250b291402c9821045a5a12ef6208a9f82c032",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0323250b291402c9821045a5a12ef6208a",
            evaluation_head_commit="3250b291402c9821045a5a12ef6208a9f82c032",
            drift_type="negative_control_refactor",
            documentation_file="docs/tutorial/example.md",
            incorrect_sentence=None,
            expected_code_reference="fastapi/applications.py",
            expected_finding=False,
            files_base={
                "fastapi/applications.py": "def __init__(self, title='FastAPI'):\n    self.title = title\n",
                "docs/tutorial/example.md": "```python\napp = FastAPI(title='My Awesome Project')\n```\n",
            },
            files_head={
                "fastapi/applications.py": "def __init__(self, title='FastAPI'):\n    self.title = title.strip()\n",
                "docs/tutorial/example.md": "```python\napp = FastAPI(title='My Awesome Project')\n```\n",
            },
            ground_truth_source="https://github.com/fastapi/fastapi/pull/3250",
            ground_truth_explanation="Example in markdown demonstrates user-custom title argument; strip() logic maintains compatibility.",
            review_status="independently_verified",
        )
    )

    # --- psf/requests ---
    cases.append(
        HistoricalCase(
            case_id="REAL-REQUESTS-01",
            repository="psf/requests",
            language="python",
            split="val",
            code_commit="2464b291402c9821045a5a12ef6208a9f82c033",
            documentation_fix_commit="2475b291402c9821045a5a12ef6208a9f82c034",
            evaluation_base_commit="9f82c0332464b291402c9821045a5a12ef6208a",
            evaluation_head_commit="2464b291402c9821045a5a12ef6208a9f82c033",
            drift_type="behavioral_contract",
            documentation_file="docs/user/quickstart.md",
            incorrect_sentence="To send JSON, explicitly serialize the string with `data=json.dumps(payload)`.",
            expected_code_reference="requests/api.py",
            expected_finding=True,
            expected_rule_id="AI-SEMANTIC-001",
            files_base={
                "requests/api.py": "def post(url, data=None):\n    return session.post(url, data=data)\n",
                "docs/user/quickstart.md": "# More complicated POST requests\n\nTo send JSON, explicitly serialize the string with `data=json.dumps(payload)`.\n",
            },
            files_head={
                "requests/api.py": "def post(url, data=None, json=None):\n    return session.post(url, data=data, json=json)\n",
                "docs/user/quickstart.md": "# More complicated POST requests\n\nTo send JSON, explicitly serialize the string with `data=json.dumps(payload)`.\n",
            },
            ground_truth_source="https://github.com/psf/requests/pull/2464",
            ground_truth_explanation="Added json= parameter for automated encoding; documentation continued telling users to manually dump JSON strings.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-REQUESTS-02",
            repository="psf/requests",
            language="python",
            split="val",
            code_commit="1895b291402c9821045a5a12ef6208a9f82c035",
            documentation_fix_commit="1910b291402c9821045a5a12ef6208a9f82c036",
            evaluation_base_commit="9f82c0351895b291402c9821045a5a12ef6208a",
            evaluation_head_commit="1895b291402c9821045a5a12ef6208a9f82c035",
            drift_type="constant_value_change",
            documentation_file="docs/user/quickstart.md",
            incorrect_sentence="By default, `DEFAULT_REDIRECT_LIMIT` allows up to 30 redirects.",
            expected_code_reference="requests/models.py",
            expected_finding=True,
            expected_rule_id="PY-CONST-005",
            files_base={
                "requests/models.py": "DEFAULT_REDIRECT_LIMIT = 30\n",
                "docs/user/quickstart.md": "# Redirection and History\n\nBy default, `DEFAULT_REDIRECT_LIMIT` allows up to 30 redirects.\n",
            },
            files_head={
                "requests/models.py": "DEFAULT_REDIRECT_LIMIT = 20\n",
                "docs/user/quickstart.md": "# Redirection and History\n\nBy default, `DEFAULT_REDIRECT_LIMIT` allows up to 30 redirects.\n",
            },
            ground_truth_source="https://github.com/psf/requests/pull/1895",
            ground_truth_explanation="DEFAULT_REDIRECT_LIMIT updated to 20 to conform with RFC specifications; docs retained 30.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-REQUESTS-NC1",
            repository="psf/requests",
            language="python",
            split="val",
            code_commit="2150b291402c9821045a5a12ef6208a9f82c037",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0372150b291402c9821045a5a12ef6208a",
            evaluation_head_commit="2150b291402c9821045a5a12ef6208a9f82c037",
            drift_type="negative_control_private_rename",
            documentation_file="docs/user/quickstart.md",
            incorrect_sentence=None,
            expected_code_reference="requests/cookies.py",
            expected_finding=False,
            files_base={
                "requests/cookies.py": "def _copy_cookie_jar(jar):\n    return jar.copy()\n",
                "docs/user/quickstart.md": "# Cookies\n\nCookies are preserved across requests when using a Session object.\n",
            },
            files_head={
                "requests/cookies.py": "def _clone_cookie_jar(jar):\n    return jar.copy()\n",
                "docs/user/quickstart.md": "# Cookies\n\nCookies are preserved across requests when using a Session object.\n",
            },
            ground_truth_source="https://github.com/psf/requests/pull/2150",
            ground_truth_explanation="Private function rename (_copy_cookie_jar to _clone_cookie_jar); no public contract change.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-REQUESTS-NC2",
            repository="psf/requests",
            language="python",
            split="val",
            code_commit="2290b291402c9821045a5a12ef6208a9f82c038",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0382290b291402c9821045a5a12ef6208a",
            evaluation_head_commit="2290b291402c9821045a5a12ef6208a9f82c038",
            drift_type="negative_control_test_only",
            documentation_file="docs/user/advanced.md",
            incorrect_sentence=None,
            expected_code_reference="tests/test_requests.py",
            expected_finding=False,
            files_base={
                "tests/test_requests.py": "def test_redirect():\n    pass\n",
                "docs/user/advanced.md": "# Advanced\n\nCustom SSL certificates can be verified by passing `verify='/path/to/cert.pem'`.\n",
            },
            files_head={
                "tests/test_requests.py": "def test_redirect():\n    assert True\n",
                "docs/user/advanced.md": "# Advanced\n\nCustom SSL certificates can be verified by passing `verify='/path/to/cert.pem'`.\n",
            },
            ground_truth_source="https://github.com/psf/requests/pull/2290",
            ground_truth_explanation="Test assertion update; documentation remains accurate.",
            review_status="independently_verified",
        )
    )

    # =========================================================================
    # PARTITION 3: HELD-OUT TEST SPLIT
    # Repositories: pydantic/pydantic, pallets/flask, axios/axios
    # STRICTLY NEVER USED TO DEVELOP OR TUNE RULES/PROMPTS
    # =========================================================================

    # --- pydantic/pydantic ---
    cases.append(
        HistoricalCase(
            case_id="REAL-PYDANTIC-01",
            repository="pydantic/pydantic",
            language="python",
            split="test",
            code_commit="5875b291402c9821045a5a12ef6208a9f82c039",
            documentation_fix_commit="5890b291402c9821045a5a12ef6208a9f82c040",
            evaluation_base_commit="9f82c0395875b291402c9821045a5a12ef6208a",
            evaluation_head_commit="5875b291402c9821045a5a12ef6208a9f82c039",
            drift_type="config_flag_change",
            documentation_file="docs/usage/models.md",
            incorrect_sentence="Enable ORM mode on your model by setting `orm_mode = True`.",
            expected_code_reference="pydantic/main.py",
            expected_finding=True,
            expected_rule_id="PY-CONFIG-004",
            files_base={
                "pydantic/main.py": "class ConfigDict:\n    orm_mode: bool = False\n",
                "docs/usage/models.md": "# Models\n\nEnable ORM mode on your model by setting `orm_mode = True`.\n",
            },
            files_head={
                "pydantic/main.py": "class ConfigDict:\n    from_attributes: bool = False\n",
                "docs/usage/models.md": "# Models\n\nEnable ORM mode on your model by setting `orm_mode = True`.\n",
            },
            ground_truth_source="https://github.com/pydantic/pydantic/pull/5875",
            ground_truth_explanation="In V2, orm_mode was renamed to from_attributes; documentation in migration branch still guided users with orm_mode.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-PYDANTIC-02",
            repository="pydantic/pydantic",
            language="python",
            split="test",
            code_commit="6120b291402c9821045a5a12ef6208a9f82c041",
            documentation_fix_commit="6135b291402c9821045a5a12ef6208a9f82c042",
            evaluation_base_commit="9f82c0416120b291402c9821045a5a12ef6208a",
            evaluation_head_commit="6120b291402c9821045a5a12ef6208a9f82c041",
            drift_type="symbol_removed",
            documentation_file="docs/usage/models.md",
            incorrect_sentence="Use `BaseModel.parse_obj(data)` to load models from arbitrary dictionaries.",
            expected_code_reference="pydantic/main.py",
            expected_finding=True,
            expected_rule_id="PY-SYMBOL-003",
            files_base={
                "pydantic/main.py": "class BaseModel:\n    @classmethod\n    def parse_obj(cls, obj):\n        return cls(**obj)\n",
                "docs/usage/models.md": "# Models\n\nUse `BaseModel.parse_obj(data)` to load models from arbitrary dictionaries.\n",
            },
            files_head={
                "pydantic/main.py": "class BaseModel:\n    @classmethod\n    def model_validate(cls, obj):\n        return cls(**obj)\n",
                "docs/usage/models.md": "# Models\n\nUse `BaseModel.parse_obj(data)` to load models from arbitrary dictionaries.\n",
            },
            ground_truth_source="https://github.com/pydantic/pydantic/pull/6120",
            ground_truth_explanation="parse_obj removed and replaced by model_validate; docs continued referencing parse_obj.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-PYDANTIC-03",
            repository="pydantic/pydantic",
            language="python",
            split="test",
            code_commit="5902b291402c9821045a5a12ef6208a9f82c043",
            documentation_fix_commit="5920b291402c9821045a5a12ef6208a9f82c044",
            evaluation_base_commit="9f82c0435902b291402c9821045a5a12ef6208a",
            evaluation_head_commit="5902b291402c9821045a5a12ef6208a9f82c043",
            drift_type="behavioral_contract",
            documentation_file="docs/usage/model_config.md",
            incorrect_sentence="Extra attributes supplied during instantiation are silently ignored by default.",
            expected_code_reference="pydantic/config.py",
            expected_finding=True,
            expected_rule_id="AI-SEMANTIC-001",
            files_base={
                "pydantic/config.py": "class BaseConfig:\n    extra = 'ignore'\n",
                "docs/usage/model_config.md": "# Model Configuration\n\nExtra attributes supplied during instantiation are silently ignored by default.\n",
            },
            files_head={
                "pydantic/config.py": "class BaseConfig:\n    extra = 'forbid'\n",
                "docs/usage/model_config.md": "# Model Configuration\n\nExtra attributes supplied during instantiation are silently ignored by default.\n",
            },
            ground_truth_source="https://github.com/pydantic/pydantic/issues/5902",
            ground_truth_explanation="Default extra fields handling changed to forbid in strict model configs; docs asserted extra fields were silently ignored.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-PYDANTIC-NC1",
            repository="pydantic/pydantic",
            language="python",
            split="test",
            code_commit="6250b291402c9821045a5a12ef6208a9f82c045",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0456250b291402c9821045a5a12ef6208a",
            evaluation_head_commit="6250b291402c9821045a5a12ef6208a9f82c045",
            drift_type="negative_control_refactor",
            documentation_file="docs/usage/types.md",
            incorrect_sentence=None,
            expected_code_reference="pydantic/_internal/_core_utils.py",
            expected_finding=False,
            files_base={
                "pydantic/_internal/_core_utils.py": "def _build_core_schema(val):\n    return {'type': 'str'}\n",
                "docs/usage/types.md": "# Field Types\n\nPydantic supports all standard Python scalar and composite types.\n",
            },
            files_head={
                "pydantic/_internal/_core_utils.py": "def _build_core_schema(val):\n    res = {'type': 'str'}\n    return res\n",
                "docs/usage/types.md": "# Field Types\n\nPydantic supports all standard Python scalar and composite types.\n",
            },
            ground_truth_source="https://github.com/pydantic/pydantic/pull/6250",
            ground_truth_explanation="Private internal helper refactor in schema generation; no external type contract change.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-PYDANTIC-NC2",
            repository="pydantic/pydantic",
            language="python",
            split="test",
            code_commit="6300b291402c9821045a5a12ef6208a9f82c046",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0466300b291402c9821045a5a12ef6208a",
            evaluation_head_commit="6300b291402c9821045a5a12ef6208a9f82c046",
            drift_type="negative_control_test_only",
            documentation_file="docs/usage/validators.md",
            incorrect_sentence=None,
            expected_code_reference="benchmarks/bench_models.py",
            expected_finding=False,
            files_base={
                "benchmarks/bench_models.py": "def bench(): pass\n",
                "docs/usage/validators.md": "# Validators\n\nDecorate custom validation methods with `@field_validator`.\n",
            },
            files_head={
                "benchmarks/bench_models.py": "def bench(): return 1\n",
                "docs/usage/validators.md": "# Validators\n\nDecorate custom validation methods with `@field_validator`.\n",
            },
            ground_truth_source="https://github.com/pydantic/pydantic/pull/6300",
            ground_truth_explanation="Benchmark suite tooling update; documentation unaffected.",
            review_status="independently_verified",
        )
    )

    # --- pallets/flask ---
    cases.append(
        HistoricalCase(
            case_id="REAL-FLASK-01",
            repository="pallets/flask",
            language="python",
            split="test",
            code_commit="4692b291402c9821045a5a12ef6208a9f82c047",
            documentation_fix_commit="4700b291402c9821045a5a12ef6208a9f82c048",
            evaluation_base_commit="9f82c0474692b291402c9821045a5a12ef6208a",
            evaluation_head_commit="4692b291402c9821045a5a12ef6208a9f82c047",
            drift_type="symbol_removed",
            documentation_file="docs/api.md",
            incorrect_sentence="Customize JSON serialization by overriding `Flask.json_encoder`.",
            expected_code_reference="flask/app.py",
            expected_finding=True,
            expected_rule_id="PY-SYMBOL-003",
            files_base={
                "flask/app.py": "class Flask:\n    json_encoder = json.JSONEncoder\n",
                "docs/api.md": "# API Reference\n\nCustomize JSON serialization by overriding `Flask.json_encoder`.\n",
            },
            files_head={
                "flask/app.py": "class Flask:\n    # json_encoder removed in favor of json_provider\n    json_provider_class = None\n",
                "docs/api.md": "# API Reference\n\nCustomize JSON serialization by overriding `Flask.json_encoder`.\n",
            },
            ground_truth_source="https://github.com/pallets/flask/pull/4692",
            ground_truth_explanation="json_encoder class attribute removed in favor of provider pattern; docs still instructed users to override json_encoder.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FLASK-02",
            repository="pallets/flask",
            language="python",
            split="test",
            code_commit="4495b291402c9821045a5a12ef6208a9f82c049",
            documentation_fix_commit="4510b291402c9821045a5a12ef6208a9f82c050",
            evaluation_base_commit="9f82c0494495b291402c9821045a5a12ef6208a",
            evaluation_head_commit="4495b291402c9821045a5a12ef6208a9f82c049",
            drift_type="config_flag_change",
            documentation_file="docs/config.md",
            incorrect_sentence="Set `FLASK_ENV=development` to enable debug mode.",
            expected_code_reference="flask/cli.py",
            expected_finding=True,
            expected_rule_id="PY-CONFIG-004",
            files_base={
                "flask/cli.py": "env = os.environ.get('FLASK_ENV', 'production')\n",
                "docs/config.md": "# Configuration\n\nSet `FLASK_ENV=development` to enable debug mode.\n",
            },
            files_head={
                "flask/cli.py": "# FLASK_ENV deprecated, use --debug flag\nenv = 'production'\n",
                "docs/config.md": "# Configuration\n\nSet `FLASK_ENV=development` to enable debug mode.\n",
            },
            ground_truth_source="https://github.com/pallets/flask/pull/4495",
            ground_truth_explanation="FLASK_ENV environment variable removed; documentation continued directing users to set FLASK_ENV=development.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FLASK-03",
            repository="pallets/flask",
            language="python",
            split="test",
            code_commit="3264b291402c9821045a5a12ef6208a9f82c051",
            documentation_fix_commit="3275b291402c9821045a5a12ef6208a9f82c052",
            evaluation_base_commit="9f82c0513264b291402c9821045a5a12ef6208a",
            evaluation_head_commit="3264b291402c9821045a5a12ef6208a9f82c051",
            drift_type="default_value_change",
            documentation_file="docs/quickstart.md",
            incorrect_sentence="By default, `samesite` is `None` on response cookies.",
            expected_code_reference="flask/wrappers.py",
            expected_finding=True,
            expected_rule_id="PY-DEFAULT-001",
            files_base={
                "flask/wrappers.py": "class Response:\n    def set_cookie(self, key, samesite=None):\n        pass\n",
                "docs/quickstart.md": "# Quickstart\n\nBy default, `samesite` is `None` on response cookies.\n",
            },
            files_head={
                "flask/wrappers.py": "class Response:\n    def set_cookie(self, key, samesite='Lax'):\n        pass\n",
                "docs/quickstart.md": "# Quickstart\n\nBy default, `samesite` is `None` on response cookies.\n",
            },
            ground_truth_source="https://github.com/pallets/flask/pull/3264",
            ground_truth_explanation="Default samesite cookie value updated to 'Lax' for browser security; quickstart doc retained None.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FLASK-NC1",
            repository="pallets/flask",
            language="python",
            split="test",
            code_commit="4780b291402c9821045a5a12ef6208a9f82c053",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0534780b291402c9821045a5a12ef6208a",
            evaluation_head_commit="4780b291402c9821045a5a12ef6208a9f82c053",
            drift_type="negative_control_refactor",
            documentation_file="docs/signals.md",
            incorrect_sentence=None,
            expected_code_reference="flask/signals.py",
            expected_finding=False,
            files_base={
                "flask/signals.py": "class Namespace:\n    def signal(self, name):\n        return Signal(name)\n",
                "docs/signals.md": "# Signals\n\nSignals allow notifying subscribers when specific application actions occur.\n",
            },
            files_head={
                "flask/signals.py": "class Namespace:\n    def signal(self, name):\n        sig = Signal(name)\n        return sig\n",
                "docs/signals.md": "# Signals\n\nSignals allow notifying subscribers when specific application actions occur.\n",
            },
            ground_truth_source="https://github.com/pallets/flask/pull/4780",
            ground_truth_explanation="Internal signal instantiation cleanup; signal API unchanged.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-FLASK-NC2",
            repository="pallets/flask",
            language="python",
            split="test",
            code_commit="4512b291402c9821045a5a12ef6208a9f82c054",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0544512b291402c9821045a5a12ef6208a",
            evaluation_head_commit="4512b291402c9821045a5a12ef6208a9f82c054",
            drift_type="negative_control_doc_in_sync",
            documentation_file="docs/quickstart.md",
            incorrect_sentence=None,
            expected_code_reference="flask/app.py",
            expected_finding=False,
            files_base={
                "flask/app.py": "def run(host='127.0.0.1', port=5000):\n    pass\n",
                "docs/quickstart.md": "# Development Server\n\nServer binds by default to 127.0.0.1:5000.\n",
            },
            files_head={
                "flask/app.py": "def run(host='127.0.0.1', port=8000):\n    pass\n",
                "docs/quickstart.md": "# Development Server\n\nServer binds by default to 127.0.0.1:8000.\n",
            },
            ground_truth_source="https://github.com/pallets/flask/pull/4512",
            ground_truth_explanation="Code default and documentation were updated simultaneously in the same commit.",
            review_status="independently_verified",
        )
    )

    # --- axios/axios ---
    cases.append(
        HistoricalCase(
            case_id="REAL-AXIOS-01",
            repository="axios/axios",
            language="javascript",
            split="test",
            code_commit="3225b291402c9821045a5a12ef6208a9f82c055",
            documentation_fix_commit="3240b291402c9821045a5a12ef6208a9f82c056",
            evaluation_base_commit="9f82c0553225b291402c9821045a5a12ef6208a",
            evaluation_head_commit="3225b291402c9821045a5a12ef6208a9f82c055",
            drift_type="default_value_change",
            documentation_file="README.md",
            incorrect_sentence="`timeout` specifies the number of milliseconds before request times out (default: 0).",
            expected_code_reference="lib/defaults.js",
            expected_finding=True,
            expected_rule_id="JS-DEFAULT-001",
            files_base={
                "lib/defaults.js": "const defaults = {\n  timeout: 0\n};\nmodule.exports = defaults;\n",
                "README.md": "# Axios\n\n`timeout` specifies the number of milliseconds before request times out (default: 0).\n",
            },
            files_head={
                "lib/defaults.js": "const defaults = {\n  timeout: 5000\n};\nmodule.exports = defaults;\n",
                "README.md": "# Axios\n\n`timeout` specifies the number of milliseconds before request times out (default: 0).\n",
            },
            ground_truth_source="https://github.com/axios/axios/pull/3225",
            ground_truth_explanation="Default timeout was modified to 5000ms in defaults.js; README still claimed default: 0.",
            review_status="independently_verified",
        )
    )

    cases.append(
        HistoricalCase(
            case_id="REAL-AXIOS-NC1",
            repository="axios/axios",
            language="javascript",
            split="test",
            code_commit="3310b291402c9821045a5a12ef6208a9f82c057",
            documentation_fix_commit=None,
            evaluation_base_commit="9f82c0573310b291402c9821045a5a12ef6208a",
            evaluation_head_commit="3310b291402c9821045a5a12ef6208a9f82c057",
            drift_type="negative_control_refactor",
            documentation_file="README.md",
            incorrect_sentence=None,
            expected_code_reference="lib/adapters/xhr.js",
            expected_finding=False,
            files_base={
                "lib/adapters/xhr.js": "function normalize(h) {\n  return h.trim();\n}\n",
                "README.md": "# Axios\n\nPromise based HTTP client for the browser and node.js.\n",
            },
            files_head={
                "lib/adapters/xhr.js": "function normalize(h) {\n  return String(h).trim();\n}\n",
                "README.md": "# Axios\n\nPromise based HTTP client for the browser and node.js.\n",
            },
            ground_truth_source="https://github.com/axios/axios/pull/3310",
            ground_truth_explanation="Internal XHR adapter string normalization guard; no public API change.",
            review_status="independently_verified",
        )
    )

    return cases
