from docguard.extractors.python_ast import compare_python_facts, extract_python_module_facts


def test_ast_default_changed() -> None:
    before = "def connect(timeout=30):\n    return True\n"
    after = "def connect(timeout=60):\n    return True\n"
    facts = compare_python_facts("src/client.py", before, after)
    assert len(facts) == 1
    fact = facts[0]
    assert fact.kind == "default_changed"
    assert fact.symbol == "connect"
    assert fact.member == "timeout"
    assert fact.before == "30"
    assert fact.after == "60"
    assert fact.line_before == 1
    assert fact.line_after == 1


def test_ast_parameter_added_and_removed() -> None:
    before = "def login(username, password):\n    pass\n"
    after = "def login(email, password, remember=False):\n    pass\n"
    facts = compare_python_facts("src/auth.py", before, after)
    kinds = [f.kind for f in facts]
    assert "parameter_removed" in kinds
    assert "parameter_added" in kinds

    rem = next(f for f in facts if f.kind == "parameter_removed")
    assert rem.member == "username"

    add = next(f for f in facts if f.kind == "parameter_added" and f.member == "email")
    assert add.member == "email"


def test_ast_constant_changed() -> None:
    before = "MAX_CONNECTIONS = 10\n"
    after = "MAX_CONNECTIONS = 25\n"
    facts = compare_python_facts("src/settings.py", before, after)
    assert len(facts) == 1
    assert facts[0].kind == "constant_changed"
    assert facts[0].before == "10"
    assert facts[0].after == "25"


def test_ast_cli_flag_changed() -> None:
    before = """
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--timeout", default=30)
"""
    after = """
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--request-timeout", default=60)
"""
    facts = compare_python_facts("src/cli.py", before, after)
    flag_facts = [f for f in facts if f.kind == "config_flag_changed"]
    assert len(flag_facts) >= 1


def test_ast_syntax_error_emits_parse_warning() -> None:
    bad_code = "def invalid syntax : :\n"
    facts = extract_python_module_facts("bad.py", bad_code)
    assert len(facts.parse_warnings) == 1
    assert "SyntaxError" in facts.parse_warnings[0]
