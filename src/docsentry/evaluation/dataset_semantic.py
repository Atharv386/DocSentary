from docsentry.evaluation.models import EvaluationCase


def get_semantic_evaluation_cases() -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []

    # 1. Return shape / exception contract
    cases.append(
        EvaluationCase(
            case_id="SEM-01",
            category="confirmed_drift",
            name="returns_empty_list_instead_of_exception",
            description="Function get_users() now returns [] when empty instead of raising NotFoundError.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/users.py": (
                    "class NotFoundError(Exception): pass\n\n"
                    "def get_users(query):\n"
                    "    res = db_find(query)\n"
                    "    if not res:\n"
                    "        raise NotFoundError('No matching users')\n"
                    "    return res\n"
                ),
                "docs/users.md": (
                    "# Users API\n"
                    "`get_users()` raises `NotFoundError` if no matching users are found.\n"
                ),
            },
            files_head={
                "src/users.py": (
                    "class NotFoundError(Exception): pass\n\n"
                    "def get_users(query):\n"
                    "    res = db_find(query)\n"
                    "    if not res:\n"
                    "        return []\n"
                    "    return res\n"
                ),
                "docs/users.md": (
                    "# Users API\n"
                    "`get_users()` raises `NotFoundError` if no matching users are found.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/users.md",
            rationale="Code returns empty list, doc claims it raises NotFoundError.",
        )
    )

    # 2. Return None vs Empty List
    cases.append(
        EvaluationCase(
            case_id="SEM-02",
            category="confirmed_drift",
            name="returns_none_instead_of_list",
            description="list_items() now returns None when missing instead of empty list.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/catalog.py": (
                    "def list_items(category):\n"
                    "    items = store.get(category)\n"
                    "    return items if items is not None else []\n"
                ),
                "docs/catalog.md": (
                    "# Catalog\n"
                    "`list_items()` always returns a list, which will be empty if none match.\n"
                ),
            },
            files_head={
                "src/catalog.py": (
                    "def list_items(category):\n"
                    "    items = store.get(category)\n"
                    "    return items if items is not None else None\n"
                ),
                "docs/catalog.md": (
                    "# Catalog\n"
                    "`list_items()` always returns a list, which will be empty if none match.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/catalog.md",
            rationale="Doc guarantees function always returns a list, but code now returns None.",
        )
    )

    # 3. Silent error handling vs exception
    cases.append(
        EvaluationCase(
            case_id="SEM-03",
            category="confirmed_drift",
            name="silent_fallback_on_error",
            description="fetch_data() swallows ConnectionError and returns fallback.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/remote.py": ("def fetch_data(url):\n    return http_get(url)\n"),
                "docs/remote.md": (
                    "# Remote\nRaises `ConnectionError` if the remote server cannot be reached.\n"
                ),
            },
            files_head={
                "src/remote.py": (
                    "def fetch_data(url):\n"
                    "    try:\n"
                    "        return http_get(url)\n"
                    "    except ConnectionError:\n"
                    "        return {}\n"
                ),
                "docs/remote.md": (
                    "# Remote\nRaises `ConnectionError` if the remote server cannot be reached.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/remote.md",
            rationale="Doc says ConnectionError is raised; code catches it and returns empty dict.",
        )
    )

    # 4. Retry behavior removed
    cases.append(
        EvaluationCase(
            case_id="SEM-04",
            category="confirmed_drift",
            name="retries_removed",
            description="Client removed automatic retries loop; fails immediately on first attempt.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/client.py": (
                    "def send_message(msg):\n"
                    "    for _ in range(3):\n"
                    "        if try_send(msg): return True\n"
                    "    return False\n"
                ),
                "docs/client.md": (
                    "# Client\n"
                    "Automatically retries message delivery up to 3 times on transient failure.\n"
                ),
            },
            files_head={
                "src/client.py": ("def send_message(msg):\n    return try_send(msg)\n"),
                "docs/client.md": (
                    "# Client\n"
                    "Automatically retries message delivery up to 3 times on transient failure.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/client.md",
            rationale="Doc promises automatic 3-retry attempt, but loop was completely removed.",
        )
    )

    # 5. Sync to Async function
    cases.append(
        EvaluationCase(
            case_id="SEM-05",
            category="confirmed_drift",
            name="sync_to_async_conversion",
            description="load_config() turned into an async coroutine.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/loader.py": ("def load_config(path):\n    return read_sync(path)\n"),
                "docs/loader.md": (
                    "# Loader\n`load_config()` is a synchronous blocking function call.\n"
                ),
            },
            files_head={
                "src/loader.py": (
                    "async def load_config(path):\n    return await read_async(path)\n"
                ),
                "docs/loader.md": (
                    "# Loader\n`load_config()` is a synchronous blocking function call.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/loader.md",
            rationale="Doc says load_config is synchronous, but code was changed to async def.",
        )
    )

    # 6. In-memory caching removed
    cases.append(
        EvaluationCase(
            case_id="SEM-06",
            category="confirmed_drift",
            name="in_memory_cache_removed",
            description="Cache dictionary removed; compute_metrics() always recalculates.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/analytics.py": (
                    "CACHE = {}\n"
                    "def compute_metrics(dataset_id):\n"
                    "    if dataset_id not in CACHE:\n"
                    "        CACHE[dataset_id] = calculate(dataset_id)\n"
                    "    return CACHE[dataset_id]\n"
                ),
                "docs/analytics.md": (
                    "# Analytics\n"
                    "`compute_metrics()` caches results in memory across subsequent calls.\n"
                ),
            },
            files_head={
                "src/analytics.py": (
                    "def compute_metrics(dataset_id):\n    return calculate(dataset_id)\n"
                ),
                "docs/analytics.md": (
                    "# Analytics\n"
                    "`compute_metrics()` caches results in memory across subsequent calls.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/analytics.md",
            rationale="Caching logic removed from compute_metrics(), doc still claims memory caching.",
        )
    )

    # 7. Authentication required
    cases.append(
        EvaluationCase(
            case_id="SEM-07",
            category="confirmed_drift",
            name="authentication_required",
            description="get_status() now checks auth token.",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/status.py": ("def get_status(req):\n    return {'status': 'healthy'}\n"),
                "docs/status.md": (
                    "# Status\n"
                    "The `get_status` endpoint is completely unauthenticated and public.\n"
                ),
            },
            files_head={
                "src/status.py": (
                    "def get_status(req):\n"
                    "    if not req.headers.get('Authorization'):\n"
                    "        raise PermissionError('Unauthorized')\n"
                    "    return {'status': 'healthy'}\n"
                ),
                "docs/status.md": (
                    "# Status\n"
                    "The `get_status` endpoint is completely unauthenticated and public.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/status.md",
            rationale="Doc says status is unauthenticated and public; code now enforces Authorization header.",
        )
    )

    # 8. Idempotency guarantee broken
    cases.append(
        EvaluationCase(
            case_id="SEM-08",
            category="confirmed_drift",
            name="idempotency_broken",
            description="apply_update() now increments counter instead of setting state.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/state.py": ("def apply_update(val):\n    state['current'] = val\n"),
                "docs/state.md": (
                    "# State Updates\n"
                    "`apply_update()` is an idempotent operation; repeating calls with identical values produces the same state.\n"
                ),
            },
            files_head={
                "src/state.py": (
                    "def apply_update(val):\n"
                    "    state['current'] = val\n"
                    "    state['revision'] += 1\n"
                ),
                "docs/state.md": (
                    "# State Updates\n"
                    "`apply_update()` is an idempotent operation; repeating calls with identical values produces the same state.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/state.md",
            rationale="Revision counter increment makes repeating identical calls mutate state, breaking idempotency claim.",
        )
    )

    # 9. Concurrency changed to sequential
    cases.append(
        EvaluationCase(
            case_id="SEM-09",
            category="confirmed_drift",
            name="concurrency_to_sequential",
            description="process_batch() changed from ThreadPoolExecutor to sequential for loop.",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/batch.py": (
                    "from concurrent.futures import ThreadPoolExecutor\n"
                    "def process_batch(items):\n"
                    "    with ThreadPoolExecutor() as ex:\n"
                    "        return list(ex.map(handle, items))\n"
                ),
                "docs/batch.md": (
                    "# Batch Processing\n"
                    "`process_batch()` processes all items in parallel using a thread pool.\n"
                ),
            },
            files_head={
                "src/batch.py": (
                    "def process_batch(items):\n    return [handle(item) for item in items]\n"
                ),
                "docs/batch.md": (
                    "# Batch Processing\n"
                    "`process_batch()` processes all items in parallel using a thread pool.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/batch.md",
            rationale="Doc promises parallel thread pool processing; code was replaced with sequential list comprehension.",
        )
    )

    # 10. Specific Exception Type changed
    cases.append(
        EvaluationCase(
            case_id="SEM-10",
            category="confirmed_drift",
            name="exception_type_changed",
            description="parse_payload() raises ParseSyntaxError instead of ValueError.",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/parser.py": (
                    "def parse_payload(raw):\n"
                    "    if not raw.startswith('{'):\n"
                    "        raise ValueError('Invalid JSON prefix')\n"
                    "    return loads(raw)\n"
                ),
                "docs/parser.md": (
                    "# Parser\n`parse_payload()` raises `ValueError` if the input is malformed.\n"
                ),
            },
            files_head={
                "src/parser.py": (
                    "class ParseSyntaxError(Exception): pass\n\n"
                    "def parse_payload(raw):\n"
                    "    if not raw.startswith('{'):\n"
                    "        raise ParseSyntaxError('Invalid JSON prefix')\n"
                    "    return loads(raw)\n"
                ),
                "docs/parser.md": (
                    "# Parser\n`parse_payload()` raises `ValueError` if the input is malformed.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/parser.md",
            rationale="Exception type changed from ValueError to custom ParseSyntaxError, doc specifically promised ValueError.",
        )
    )

    # 11. Pagination page limit changed in logic
    cases.append(
        EvaluationCase(
            case_id="SEM-11",
            category="confirmed_drift",
            name="pagination_limit_changed",
            description="paginate() caps page size at 100 instead of 50.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/pagination.py": (
                    "def paginate(items, limit=None):\n"
                    "    cap = min(limit or 50, 50)\n"
                    "    return items[:cap]\n"
                ),
                "docs/pagination.md": (
                    "# Pagination\nThe maximum page limit enforced by `paginate()` is 50 items.\n"
                ),
            },
            files_head={
                "src/pagination.py": (
                    "def paginate(items, limit=None):\n"
                    "    cap = min(limit or 100, 100)\n"
                    "    return items[:cap]\n"
                ),
                "docs/pagination.md": (
                    "# Pagination\nThe maximum page limit enforced by `paginate()` is 50 items.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/pagination.md",
            rationale="Internal cap changed to 100 items, doc asserts maximum page limit is 50.",
        )
    )

    # 12. Rate limiting added
    cases.append(
        EvaluationCase(
            case_id="SEM-12",
            category="confirmed_drift",
            name="rate_limiting_enforced",
            description="Rate limiter added to invoke_handler().",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/handler.py": ("def invoke_handler(ctx):\n    return ctx.run()\n"),
                "docs/handler.md": (
                    "# Handler\nThere are no rate limits imposed on `invoke_handler()` calls.\n"
                ),
            },
            files_head={
                "src/handler.py": (
                    "def invoke_handler(ctx):\n"
                    "    if rate_limit_exceeded(ctx):\n"
                    "        raise TooManyRequestsError('Rate limit exceeded')\n"
                    "    return ctx.run()\n"
                ),
                "docs/handler.md": (
                    "# Handler\nThere are no rate limits imposed on `invoke_handler()` calls.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/handler.md",
            rationale="Doc says no rate limits are imposed, code explicitly checks rate limit and raises error.",
        )
    )

    # 13. Automatic rollback on error
    cases.append(
        EvaluationCase(
            case_id="SEM-13",
            category="confirmed_drift",
            name="transaction_rollback_added",
            description="Database transaction block added to save_order().",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/orders.py": (
                    "def save_order(order):\n    db.insert(order)\n    charge(order)\n"
                ),
                "docs/orders.md": (
                    "# Orders\n"
                    "Database changes in `save_order()` are not rolled back if billing fails.\n"
                ),
            },
            files_head={
                "src/orders.py": (
                    "def save_order(order):\n"
                    "    with db.transaction():\n"
                    "        db.insert(order)\n"
                    "        charge(order)\n"
                ),
                "docs/orders.md": (
                    "# Orders\n"
                    "Database changes in `save_order()` are not rolled back if billing fails.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/orders.md",
            rationale="Doc explicitly states changes are not rolled back on failure; code now uses transactional wrapper.",
        )
    )

    # 14. Logging level changed
    cases.append(
        EvaluationCase(
            case_id="SEM-14",
            category="confirmed_drift",
            name="log_level_changed_to_debug",
            description="logger.warning changed to logger.debug in notify().",
            difficulty="low",
            target_engine="ai_assisted",
            files_base={
                "src/notify.py": (
                    "import logging\n"
                    "logger = logging.getLogger(__name__)\n"
                    "def notify(event):\n"
                    "    logger.warning('Event triggered: %s', event)\n"
                ),
                "docs/notify.md": (
                    "# Notifications\n`notify()` emits a warning log to stderr for every event.\n"
                ),
            },
            files_head={
                "src/notify.py": (
                    "import logging\n"
                    "logger = logging.getLogger(__name__)\n"
                    "def notify(event):\n"
                    "    logger.debug('Event triggered: %s', event)\n"
                ),
                "docs/notify.md": (
                    "# Notifications\n`notify()` emits a warning log to stderr for every event.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/notify.md",
            rationale="Doc says warning log is emitted, code changed logger level to debug.",
        )
    )

    # 15. Encoding support restricted
    cases.append(
        EvaluationCase(
            case_id="SEM-15",
            category="confirmed_drift",
            name="encoding_restricted_utf8",
            description="export_file() hardcodes utf-8 instead of system locale.",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/export.py": (
                    "def export_file(content, encoding=None):\n"
                    "    enc = encoding or locale.getpreferredencoding()\n"
                    "    return content.encode(enc)\n"
                ),
                "docs/export.md": (
                    "# Export\n"
                    "Defaults to the system locale encoding if not explicitly specified.\n"
                ),
            },
            files_head={
                "src/export.py": (
                    "def export_file(content, encoding='utf-8'):\n"
                    "    return content.encode('utf-8')\n"
                ),
                "docs/export.md": (
                    "# Export\n"
                    "Defaults to the system locale encoding if not explicitly specified.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/export.md",
            rationale="System locale fallback was replaced with hardcoded utf-8.",
        )
    )

    # 16. Negative Control: Internal list comprehension refactor
    cases.append(
        EvaluationCase(
            case_id="SEM-16",
            category="negative_control",
            name="internal_comprehension_refactor",
            description="for loop replaced with list comprehension; returns same list.",
            difficulty="medium",
            target_engine="both",
            files_base={
                "src/utils.py": (
                    "def active_nodes(nodes):\n"
                    "    res = []\n"
                    "    for n in nodes:\n"
                    "        if n.is_active:\n"
                    "            res.append(n)\n"
                    "    return res\n"
                ),
                "docs/utils.md": (
                    "# Utilities\n`active_nodes()` returns a list of all currently active nodes.\n"
                ),
            },
            files_head={
                "src/utils.py": (
                    "def active_nodes(nodes):\n    return [n for n in nodes if n.is_active]\n"
                ),
                "docs/utils.md": (
                    "# Utilities\n`active_nodes()` returns a list of all currently active nodes.\n"
                ),
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/utils.md",
            rationale="Refactoring from for-loop to list comprehension preserves contract; doc statement remains true.",
        )
    )

    # 17. Negative Control: Internal helper function added
    cases.append(
        EvaluationCase(
            case_id="SEM-17",
            category="negative_control",
            name="internal_helper_added",
            description="Helper function _validate() extracted; public API contract unchanged.",
            difficulty="low",
            target_engine="both",
            files_base={
                "src/auth.py": (
                    "def authenticate(token):\n"
                    "    if not token or len(token) < 8: return False\n"
                    "    return verify(token)\n"
                ),
                "docs/auth.md": (
                    "# Authentication\n"
                    "`authenticate()` validates the token and returns True if valid.\n"
                ),
            },
            files_head={
                "src/auth.py": (
                    "def _validate(token):\n"
                    "    return bool(token and len(token) >= 8)\n\n"
                    "def authenticate(token):\n"
                    "    if not _validate(token): return False\n"
                    "    return verify(token)\n"
                ),
                "docs/auth.md": (
                    "# Authentication\n"
                    "`authenticate()` validates the token and returns True if valid.\n"
                ),
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/auth.md",
            rationale="Adding private helper does not alter authenticate() public contract.",
        )
    )

    # 18. Negative Control: Hypothetical Code Example
    cases.append(
        EvaluationCase(
            case_id="SEM-18",
            category="negative_control",
            name="doc_code_example_custom_arg",
            description="Documentation illustrates custom timeout=99 in usage example.",
            difficulty="medium",
            target_engine="both",
            files_base={
                "src/client.py": ("def connect(timeout=30):\n    return True\n"),
                "docs/client.md": (
                    "# Client Example\n"
                    "```python\n"
                    "# You can provide a custom timeout\n"
                    "client = connect(timeout=99)\n"
                    "```\n"
                ),
            },
            files_head={
                "src/client.py": ("def connect(timeout=45):\n    return True\n"),
                "docs/client.md": (
                    "# Client Example\n"
                    "```python\n"
                    "# You can provide a custom timeout\n"
                    "client = connect(timeout=99)\n"
                    "```\n"
                ),
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/client.md",
            rationale="Markdown block is an illustrative code example, not an assertion about the default value.",
        )
    )

    # 19. Negative Control: Historical context in doc
    cases.append(
        EvaluationCase(
            case_id="SEM-19",
            category="negative_control",
            name="doc_historical_version_note",
            description="Doc explicitly explains legacy version behavior in release notes.",
            difficulty="medium",
            target_engine="both",
            files_base={
                "src/api.py": ("def fetch_record(record_id):\n    return db.query(record_id)\n"),
                "docs/changelog.md": (
                    "# Changelog\nIn version 1.0, `fetch_record()` returned a raw tuple.\n"
                ),
            },
            files_head={
                "src/api.py": (
                    "def fetch_record(record_id):\n"
                    "    record = db.query(record_id)\n"
                    "    return RecordObject(record)\n"
                ),
                "docs/changelog.md": (
                    "# Changelog\nIn version 1.0, `fetch_record()` returned a raw tuple.\n"
                ),
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/changelog.md",
            rationale="Doc is explicitly historical changelog text referring to version 1.0.",
        )
    )

    # 20. Negative Control: Local variable rename
    cases.append(
        EvaluationCase(
            case_id="SEM-20",
            category="negative_control",
            name="local_variable_rename",
            description="Variable total renamed to sum_val in compute(); doc describes behavior.",
            difficulty="low",
            target_engine="both",
            files_base={
                "src/math_ops.py": (
                    "def compute(values):\n    total = sum(values)\n    return total * 2\n"
                ),
                "docs/math_ops.md": (
                    "# Math\n`compute()` returns double the sum of the provided values.\n"
                ),
            },
            files_head={
                "src/math_ops.py": (
                    "def compute(values):\n    sum_val = sum(values)\n    return sum_val * 2\n"
                ),
                "docs/math_ops.md": (
                    "# Math\n`compute()` returns double the sum of the provided values.\n"
                ),
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/math_ops.md",
            rationale="Internal variable rename has no effect on external mathematical contract.",
        )
    )

    # 21. Thread-safety guarantee broken
    cases.append(
        EvaluationCase(
            case_id="SEM-21",
            category="confirmed_drift",
            name="thread_safety_lock_removed",
            description="Mutex lock removed from Counter.increment().",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/counter.py": (
                    "import threading\n"
                    "class Counter:\n"
                    "    def __init__(self):\n"
                    "        self.lock = threading.Lock()\n"
                    "        self.val = 0\n"
                    "    def increment(self):\n"
                    "        with self.lock:\n"
                    "            self.val += 1\n"
                ),
                "docs/counter.md": (
                    "# Counter\n`Counter` is thread-safe and safe for concurrent increments.\n"
                ),
            },
            files_head={
                "src/counter.py": (
                    "class Counter:\n"
                    "    def __init__(self):\n"
                    "        self.val = 0\n"
                    "    def increment(self):\n"
                    "        self.val += 1\n"
                ),
                "docs/counter.md": (
                    "# Counter\n`Counter` is thread-safe and safe for concurrent increments.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/counter.md",
            rationale="Lock was removed, breaking thread-safety guarantee.",
        )
    )

    # 22. Deprecation warning added
    cases.append(
        EvaluationCase(
            case_id="SEM-22",
            category="confirmed_drift",
            name="deprecation_warning_added",
            description="Warnings.warn(DeprecationWarning) added to old_query().",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/query.py": ("def old_query(q):\n    return execute(q)\n"),
                "docs/query.md": (
                    "# Querying\n`old_query()` is fully supported with no planned deprecation.\n"
                ),
            },
            files_head={
                "src/query.py": (
                    "import warnings\n"
                    "def old_query(q):\n"
                    "    warnings.warn('old_query is deprecated', DeprecationWarning)\n"
                    "    return execute(q)\n"
                ),
                "docs/query.md": (
                    "# Querying\n`old_query()` is fully supported with no planned deprecation.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/query.md",
            rationale="Doc says fully supported without deprecation, code issues DeprecationWarning.",
        )
    )

    # 23. Case-sensitivity altered
    cases.append(
        EvaluationCase(
            case_id="SEM-23",
            category="confirmed_drift",
            name="case_sensitivity_changed",
            description="Headers converted to lower() before lookup.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/headers.py": (
                    "def get_header(headers, name):\n    return headers.get(name)\n"
                ),
                "docs/headers.md": (
                    "# Headers\n`get_header()` performs strictly case-sensitive header lookups.\n"
                ),
            },
            files_head={
                "src/headers.py": (
                    "def get_header(headers, name):\n"
                    "    h_lower = {k.lower(): v for k, v in headers.items()}\n"
                    "    return h_lower.get(name.lower())\n"
                ),
                "docs/headers.md": (
                    "# Headers\n`get_header()` performs strictly case-sensitive header lookups.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/headers.md",
            rationale="Lookup changed to case-insensitive, contradicting case-sensitive claim.",
        )
    )

    # 24. Timeout semantics changed (total vs connect)
    cases.append(
        EvaluationCase(
            case_id="SEM-24",
            category="confirmed_drift",
            name="timeout_semantics_changed",
            description="timeout passed to connect_timeout instead of total_timeout.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/request.py": (
                    "def make_request(url, timeout=10):\n"
                    "    return session.get(url, total_timeout=timeout)\n"
                ),
                "docs/request.md": (
                    "# Requests\n"
                    "The `timeout` parameter governs the total request-response roundtrip duration.\n"
                ),
            },
            files_head={
                "src/request.py": (
                    "def make_request(url, timeout=10):\n"
                    "    return session.get(url, connect_timeout=timeout)\n"
                ),
                "docs/request.md": (
                    "# Requests\n"
                    "The `timeout` parameter governs the total request-response roundtrip duration.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/request.md",
            rationale="Timeout now only applies to connection establishment, contradicting total roundtrip claim.",
        )
    )

    # 25. Extra fields rejected vs ignored
    cases.append(
        EvaluationCase(
            case_id="SEM-25",
            category="confirmed_drift",
            name="extra_fields_forbidden",
            description="Schema validator forbids extra fields instead of ignoring them.",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/schema.py": (
                    "def validate_payload(data):\n"
                    "    return {k: data[k] for k in ('id', 'name') if k in data}\n"
                ),
                "docs/schema.md": (
                    "# Schema\nUnrecognized or extra fields in the payload are silently ignored.\n"
                ),
            },
            files_head={
                "src/schema.py": (
                    "def validate_payload(data):\n"
                    "    allowed = {'id', 'name'}\n"
                    "    if set(data.keys()) - allowed:\n"
                    "        raise ValueError('Extra fields forbidden')\n"
                    "    return data\n"
                ),
                "docs/schema.md": (
                    "# Schema\nUnrecognized or extra fields in the payload are silently ignored.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/schema.md",
            rationale="Doc says extra fields are silently ignored, code now throws ValueError on extra fields.",
        )
    )

    # 26. Negative Control: Architectural doc during file reorganization
    cases.append(
        EvaluationCase(
            case_id="SEM-26",
            category="negative_control",
            name="architectural_overview_preserved",
            description="Doc outlines high-level pipeline flow; internal helper moved to sibling module.",
            difficulty="medium",
            target_engine="both",
            files_base={
                "src/pipeline.py": ("def run_stage(x):\n    return x + 1\n"),
                "docs/arch.md": (
                    "# Architecture\n"
                    "The system processes events sequentially through a pipeline stages architecture.\n"
                ),
            },
            files_head={
                "src/pipeline.py": ("from src.stages import run_stage\n"),
                "src/stages.py": ("def run_stage(x):\n    return x + 1\n"),
                "docs/arch.md": (
                    "# Architecture\n"
                    "The system processes events sequentially through a pipeline stages architecture.\n"
                ),
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/arch.md",
            rationale="High-level architecture statement remains completely accurate after internal module refactor.",
        )
    )

    # 27. Sorting order reversed
    cases.append(
        EvaluationCase(
            case_id="SEM-27",
            category="confirmed_drift",
            name="sort_order_reversed",
            description="get_logs() sorts reverse=True (descending) instead of ascending.",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/logs.py": (
                    "def get_logs():\n    return sorted(records, key=lambda r: r.timestamp)\n"
                ),
                "docs/logs.md": (
                    "# Logs\n"
                    "`get_logs()` returns log records sorted in ascending chronological order.\n"
                ),
            },
            files_head={
                "src/logs.py": (
                    "def get_logs():\n"
                    "    return sorted(records, key=lambda r: r.timestamp, reverse=True)\n"
                ),
                "docs/logs.md": (
                    "# Logs\n"
                    "`get_logs()` returns log records sorted in ascending chronological order.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/logs.md",
            rationale="Doc promises ascending order, code sets reverse=True (descending).",
        )
    )

    # 28. Soft delete to Hard delete
    cases.append(
        EvaluationCase(
            case_id="SEM-28",
            category="confirmed_drift",
            name="soft_to_hard_delete",
            description="delete_user() executes hard SQL DELETE instead of setting deleted_at.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/user_store.py": (
                    "def delete_user(user_id):\n"
                    "    db.execute('UPDATE users SET is_deleted=1 WHERE id=?', (user_id,))\n"
                ),
                "docs/privacy.md": (
                    "# User Retention\n"
                    "User deletion is a soft delete: rows are marked deleted and retained for audit.\n"
                ),
            },
            files_head={
                "src/user_store.py": (
                    "def delete_user(user_id):\n"
                    "    db.execute('DELETE FROM users WHERE id=?', (user_id,))\n"
                ),
                "docs/privacy.md": (
                    "# User Retention\n"
                    "User deletion is a soft delete: rows are marked deleted and retained for audit.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/privacy.md",
            rationale="Doc says user deletion is a soft delete; code now executes raw DELETE FROM users.",
        )
    )

    # 29. Negative Control: Doc Markdown Formatting Change
    cases.append(
        EvaluationCase(
            case_id="SEM-29",
            category="negative_control",
            name="markdown_heading_reformat",
            description="Documentation header level changed from ## to ###.",
            difficulty="low",
            target_engine="both",
            files_base={
                "src/calc.py": "def add(a, b): return a + b\n",
                "docs/calc.md": "## Math Addition\n`add(a, b)` computes the sum of two numbers.\n",
            },
            files_head={
                "src/calc.py": "def add(a, b): return a + b\n",
                "docs/calc.md": "### Math Addition\n`add(a, b)` computes the sum of two numbers.\n",
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/calc.md",
            rationale="Markdown formatting adjustment does not constitute documentation drift.",
        )
    )

    # 30. Precedence inverted (CLI vs Environment variable)
    cases.append(
        EvaluationCase(
            case_id="SEM-30",
            category="confirmed_drift",
            name="config_precedence_inverted",
            description="resolve_port() gives env var precedence over explicit argument.",
            difficulty="high",
            target_engine="ai_assisted",
            files_base={
                "src/config_resolver.py": (
                    "def resolve_port(cli_arg=None):\n"
                    "    return cli_arg or os.environ.get('PORT') or 8080\n"
                ),
                "docs/precedence.md": (
                    "# Precedence\n"
                    "Explicit CLI arguments always take precedence over environment variables.\n"
                ),
            },
            files_head={
                "src/config_resolver.py": (
                    "def resolve_port(cli_arg=None):\n"
                    "    return os.environ.get('PORT') or cli_arg or 8080\n"
                ),
                "docs/precedence.md": (
                    "# Precedence\n"
                    "Explicit CLI arguments always take precedence over environment variables.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/precedence.md",
            rationale="Doc says CLI args take precedence over env vars; code inverted order to check env var first.",
        )
    )

    # 31. ZeroDivision handling returns float('nan') instead of error
    cases.append(
        EvaluationCase(
            case_id="SEM-31",
            category="confirmed_drift",
            name="zero_division_nan_return",
            description="divide() returns float('nan') instead of raising ZeroDivisionError.",
            difficulty="medium",
            target_engine="ai_assisted",
            files_base={
                "src/math_util.py": (
                    "def divide(a, b):\n"
                    "    if b == 0:\n"
                    "        raise ZeroDivisionError('division by zero')\n"
                    "    return a / b\n"
                ),
                "docs/math_util.md": (
                    "# Division\n`divide()` raises `ZeroDivisionError` when the divisor is zero.\n"
                ),
            },
            files_head={
                "src/math_util.py": (
                    "def divide(a, b):\n"
                    "    if b == 0:\n"
                    "        return float('nan')\n"
                    "    return a / b\n"
                ),
                "docs/math_util.md": (
                    "# Division\n`divide()` raises `ZeroDivisionError` when the divisor is zero.\n"
                ),
            },
            expected_status="DRIFT",
            expected_rule_id="AI-SEMANTIC-001",
            expected_doc_file="docs/math_util.md",
            rationale="Doc states ZeroDivisionError is raised, code now returns float('nan').",
        )
    )

    # 32. Negative Control: Migration guide with both symbols
    cases.append(
        EvaluationCase(
            case_id="SEM-32",
            category="negative_control",
            name="migration_guide_both_symbols",
            description="Doc migration guide correctly contrasts legacy and modern functions.",
            difficulty="medium",
            target_engine="both",
            files_base={
                "src/service.py": ("def send_v2(payload):\n    return push(payload)\n"),
                "docs/migration.md": (
                    "# Migration\nReplace all calls to legacy `send_v1()` with `send_v2()`.\n"
                ),
            },
            files_head={
                "src/service.py": ("def send_v2(payload):\n    return push_v2(payload)\n"),
                "docs/migration.md": (
                    "# Migration\nReplace all calls to legacy `send_v1()` with `send_v2()`.\n"
                ),
            },
            expected_status="NO_DRIFT",
            expected_doc_file="docs/migration.md",
            rationale="Mention of legacy send_v1() in a migration guide recommending send_v2() is intentional advice.",
        )
    )

    return cases
