from docsentry.contracts.code import CodeFact
from docsentry.contracts.docs import DocSpan
from docsentry.mapping.candidates import CandidateMapper
from docsentry.rules.config_flags import detect_config_flag_drift
from docsentry.rules.constants import detect_constant_drift
from docsentry.rules.defaults import detect_default_drift
from docsentry.rules.engine import DeterministicRuleEngine
from docsentry.rules.signatures import detect_signature_drift
from docsentry.rules.symbols import detect_symbol_drift


def test_rule_default_drift_positive() -> None:
    fact = CodeFact(
        fact_id="fact-1",
        language="python",
        path="src/client.py",
        qualified_name="client.connect",
        symbol="connect",
        member="timeout",
        kind="default_changed",
        before="30",
        after="60",
        line_after=12,
        source_change_id="c1",
        static_confidence="high",
    )
    span = DocSpan(
        span_id="span-1",
        path="docs/config.md",
        block_type="paragraph",
        text="The default timeout is 30 seconds.",
        raw_text="The default timeout is 30 seconds.",
        line_start=23,
        line_end=23,
        inline_code=["timeout"],
    )
    finding = detect_default_drift(fact, span, "DG-0001")
    assert finding is not None
    assert finding.status == "DRIFT"
    assert finding.rule_id == "PY-DEFAULT-001"
    assert len(finding.evidence) == 2


def test_rule_default_drift_negative_already_updated() -> None:
    fact = CodeFact(
        fact_id="fact-1",
        language="python",
        path="src/client.py",
        qualified_name="client.connect",
        symbol="connect",
        member="timeout",
        kind="default_changed",
        before="30",
        after="60",
        source_change_id="c1",
        static_confidence="high",
    )
    # Docs already updated to 60
    span = DocSpan(
        span_id="span-1",
        path="docs/config.md",
        block_type="paragraph",
        text="The default timeout is 60 seconds.",
        raw_text="The default timeout is 60 seconds.",
        line_start=23,
        line_end=23,
        inline_code=["timeout"],
    )
    finding = detect_default_drift(fact, span, "DG-0001")
    assert finding is None


def test_rule_default_drift_negative_historical_context() -> None:
    fact = CodeFact(
        fact_id="fact-1",
        language="python",
        path="src/client.py",
        symbol="connect",
        member="timeout",
        kind="default_changed",
        before="30",
        after="60",
        source_change_id="c1",
        static_confidence="high",
    )
    span = DocSpan(
        span_id="span-1",
        path="docs/config.md",
        block_type="paragraph",
        text="Previously, the timeout was 30 seconds before version 2.0.",
        raw_text="Previously, the timeout was 30 seconds before version 2.0.",
        line_start=23,
        line_end=23,
        inline_code=["timeout"],
    )
    finding = detect_default_drift(fact, span, "DG-0001")
    assert finding is None


def test_rule_param_removed() -> None:
    fact = CodeFact(
        fact_id="fact-2",
        language="python",
        path="src/auth.py",
        symbol="login",
        member="username",
        kind="parameter_removed",
        before="username",
        source_change_id="c1",
        static_confidence="high",
    )
    span = DocSpan(
        span_id="span-2",
        path="docs/auth.md",
        block_type="paragraph",
        text="Pass the `username` and password to authenticate.",
        raw_text="Pass the `username` and password to authenticate.",
        line_start=15,
        line_end=15,
        inline_code=["username"],
    )
    finding = detect_signature_drift(fact, span, "DG-0002")
    assert finding is not None
    assert finding.rule_id == "PY-PARAM-002"
    assert finding.status == "DRIFT"


def test_rule_symbol_removed() -> None:
    fact = CodeFact(
        fact_id="fact-3",
        language="python",
        path="src/api.py",
        symbol="old_login",
        kind="function_removed",
        before="old_login",
        source_change_id="c1",
        static_confidence="high",
    )
    span = DocSpan(
        span_id="span-3",
        path="docs/tutorial.md",
        block_type="paragraph",
        text="Call `old_login` to start a session.",
        raw_text="Call `old_login` to start a session.",
        line_start=10,
        line_end=10,
        inline_code=["old_login"],
    )
    finding = detect_symbol_drift(fact, span, "DG-0003")
    assert finding is not None
    assert finding.status == "POTENTIAL_DRIFT"


def test_rule_config_flag_drift() -> None:
    fact = CodeFact(
        fact_id="fact-4",
        language="python",
        path="src/cli.py",
        symbol="argparse",
        member="--timeout",
        kind="config_flag_changed",
        before="--timeout",
        source_change_id="c1",
        static_confidence="high",
    )
    span = DocSpan(
        span_id="span-4",
        path="docs/cli.md",
        block_type="table_cell",
        text="`--timeout` : Request timeout in seconds.",
        raw_text="`--timeout` : Request timeout in seconds.",
        line_start=30,
        line_end=30,
        inline_code=["--timeout"],
    )
    finding = detect_config_flag_drift(fact, span, "DG-0004")
    assert finding is not None
    assert finding.status == "DRIFT"


def test_rule_constant_drift() -> None:
    fact = CodeFact(
        fact_id="fact-5",
        language="python",
        path="src/settings.py",
        symbol="MAX_RETRIES",
        member="MAX_RETRIES",
        kind="constant_changed",
        before="3",
        after="5",
        source_change_id="c1",
        static_confidence="high",
    )
    span = DocSpan(
        span_id="span-5",
        path="docs/settings.md",
        block_type="paragraph",
        text="By default, `MAX_RETRIES` is set to 3.",
        raw_text="By default, `MAX_RETRIES` is set to 3.",
        line_start=12,
        line_end=12,
        inline_code=["MAX_RETRIES"],
    )
    finding = detect_constant_drift(fact, span, "DG-0005")
    assert finding is not None
    assert finding.status == "DRIFT"


def test_candidate_mapper_and_engine_integration() -> None:
    fact = CodeFact(
        fact_id="f1",
        language="python",
        path="src/client.py",
        qualified_name="client.connect",
        symbol="connect",
        member="timeout",
        kind="default_changed",
        before="30",
        after="60",
        line_after=12,
        source_change_id="c1",
        static_confidence="high",
    )
    span = DocSpan(
        span_id="s1",
        path="docs/config.md",
        block_type="paragraph",
        heading_path=["Client", "Networking"],
        text="The default timeout is 30 seconds.",
        raw_text="The default timeout is 30 seconds.",
        line_start=23,
        line_end=23,
        inline_code=["timeout"],
    )

    mapper = CandidateMapper()
    links = mapper.map([fact], [span])
    assert len(links) >= 1
    assert links[0].score >= 4.0

    engine = DeterministicRuleEngine()
    findings = engine.evaluate([fact], [span], links)
    assert len(findings) == 1
    assert findings[0].rule_id == "PY-DEFAULT-001"
