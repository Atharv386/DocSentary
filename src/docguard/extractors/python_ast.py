import ast
from typing import Any

from docguard.contracts.code import CodeFact


class FunctionSignature:
    def __init__(
        self,
        name: str,
        qualified_name: str,
        line_start: int,
        line_end: int,
        parameters: list[dict[str, Any]],
        decorators: list[str],
        returns: str | None = None,
    ) -> None:
        self.name = name
        self.qualified_name = qualified_name
        self.line_start = line_start
        self.line_end = line_end
        self.parameters = parameters
        self.decorators = decorators
        self.returns = returns


class ModuleFacts:
    def __init__(self, path: str) -> None:
        self.path = path
        self.functions: dict[str, FunctionSignature] = {}
        self.constants: dict[str, tuple[str, int]] = {}  # name -> (normalized_value, line)
        self.cli_flags: dict[str, tuple[str, int]] = {}  # flag -> (default_value, line)
        self.parse_warnings: list[str] = []


def _unparse_node(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


class ASTVisitor(ast.NodeVisitor):
    def __init__(self, path: str) -> None:
        self.path = path
        self.scope_stack: list[str] = []
        self.facts = ModuleFacts(path)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record_function(node)

    def _record_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        qname_parts = self.scope_stack + [node.name]
        qualified_name = ".".join(qname_parts)

        params: list[dict[str, Any]] = []

        # Positional-only args
        posonly = getattr(node.args, "posonlyargs", [])
        num_defaults = len(node.args.defaults)
        # Defaults apply from the right of posonlyargs + args
        all_regular = posonly + node.args.args
        default_offset = len(all_regular) - num_defaults

        for idx, arg in enumerate(all_regular):
            default_val = None
            if idx >= default_offset:
                def_node = node.args.defaults[idx - default_offset]
                default_val = _unparse_node(def_node)
            kind = "POSITIONAL_ONLY" if idx < len(posonly) else "POSITIONAL_OR_KEYWORD"
            params.append(
                {
                    "name": arg.arg,
                    "kind": kind,
                    "default": default_val,
                    "annotation": _unparse_node(arg.annotation),
                }
            )

        # Vararg (*args)
        if node.args.vararg:
            params.append(
                {
                    "name": f"*{node.args.vararg.arg}",
                    "kind": "VAR_POSITIONAL",
                    "default": None,
                }
            )

        # Keyword-only args
        for arg, def_node in zip(node.args.kwonlyargs, node.args.kw_defaults, strict=False):
            params.append(
                {
                    "name": arg.arg,
                    "kind": "KEYWORD_ONLY",
                    "default": _unparse_node(def_node),
                    "annotation": _unparse_node(arg.annotation),
                }
            )

        # Kwarg (**kwargs)
        if node.args.kwarg:
            params.append(
                {
                    "name": f"**{node.args.kwarg.arg}",
                    "kind": "VAR_KEYWORD",
                    "default": None,
                }
            )

        decorators = [_unparse_node(d) or "" for d in node.decorator_list]
        returns = _unparse_node(node.returns)

        sig = FunctionSignature(
            name=node.name,
            qualified_name=qualified_name,
            line_start=node.lineno,
            line_end=getattr(node, "end_lineno", node.lineno),
            parameters=params,
            decorators=decorators,
            returns=returns,
        )
        self.facts.functions[qualified_name] = sig

        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_Assign(self, node: ast.Assign) -> None:
        # Module-level constant assignment
        if not self.scope_stack:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    val = _unparse_node(node.value)
                    if val is not None:
                        self.facts.constants[target.id] = (val, node.lineno)

        # Check for argparse add_argument calls
        self._check_argparse(node.value, node.lineno)
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr) -> None:
        self._check_argparse(node.value, node.lineno)
        self.generic_visit(node)

    def _check_argparse(self, node: ast.AST, lineno: int) -> None:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "add_argument":
                flags = [ast.literal_eval(a) for a in node.args if isinstance(a, ast.Constant)]
                default_val = None
                for kw in node.keywords:
                    if kw.arg == "default":
                        default_val = _unparse_node(kw.value)
                for f in flags:
                    if isinstance(f, str) and f.startswith("-"):
                        self.facts.cli_flags[f] = (default_val or "None", lineno)


def extract_python_module_facts(path: str, source_code: str) -> ModuleFacts:
    visitor = ASTVisitor(path)
    try:
        tree = ast.parse(source_code, filename=path)
        visitor.visit(tree)
    except SyntaxError as err:
        visitor.facts.parse_warnings.append(f"SyntaxError in {path}:{err.lineno}: {err.msg}")
    except Exception as err:
        visitor.facts.parse_warnings.append(f"Parse error in {path}: {err}")
    return visitor.facts


def compare_python_facts(
    path: str,
    before_source: str | None,
    after_source: str | None,
    change_id: str = "diff",
) -> list[CodeFact]:
    """Compares before and after Python snapshots and emits CodeFact records."""
    facts: list[CodeFact] = []

    if before_source is None and after_source is None:
        return facts

    if before_source is None and after_source is not None:
        # New file added
        after_facts = extract_python_module_facts(path, after_source)
        for w in after_facts.parse_warnings:
            facts.append(
                CodeFact(
                    fact_id=f"warn-{len(facts)+1}",
                    language="python",
                    path=path,
                    kind="parse_warning",
                    before=None,
                    after=w,
                    source_change_id=change_id,
                    static_confidence="high",
                )
            )
        for qname, sig in after_facts.functions.items():
            facts.append(
                CodeFact(
                    fact_id=f"func-add-{len(facts)+1}",
                    language="python",
                    path=path,
                    qualified_name=qname,
                    symbol=sig.name,
                    kind="function_added",
                    after=sig.name,
                    line_after=sig.line_start,
                    source_change_id=change_id,
                    static_confidence="high",
                )
            )
        return facts

    if before_source is not None and after_source is None:
        # File deleted
        before_facts = extract_python_module_facts(path, before_source)
        for qname, sig in before_facts.functions.items():
            facts.append(
                CodeFact(
                    fact_id=f"func-rem-{len(facts)+1}",
                    language="python",
                    path=path,
                    qualified_name=qname,
                    symbol=sig.name,
                    kind="function_removed",
                    before=sig.name,
                    line_before=sig.line_start,
                    source_change_id=change_id,
                    static_confidence="high",
                )
            )
        return facts

    # File modified
    assert before_source is not None and after_source is not None
    before_facts = extract_python_module_facts(path, before_source)
    after_facts = extract_python_module_facts(path, after_source)

    for w in after_facts.parse_warnings:
        facts.append(
            CodeFact(
                fact_id=f"warn-{len(facts)+1}",
                language="python",
                path=path,
                kind="parse_warning",
                before=None,
                after=w,
                source_change_id=change_id,
                static_confidence="high",
            )
        )

    # 1. Compare functions
    for qname, before_sig in before_facts.functions.items():
        if qname not in after_facts.functions:
            facts.append(
                CodeFact(
                    fact_id=f"func-rem-{len(facts)+1}",
                    language="python",
                    path=path,
                    qualified_name=qname,
                    symbol=before_sig.name,
                    kind="function_removed",
                    before=before_sig.name,
                    line_before=before_sig.line_start,
                    source_change_id=change_id,
                    static_confidence="high",
                )
            )
            continue

        after_sig = after_facts.functions[qname]

        # Map parameters by name
        before_params = {p["name"]: p for p in before_sig.parameters}
        after_params = {p["name"]: p for p in after_sig.parameters}

        # Check default value changes
        for pname, b_param in before_params.items():
            if pname in after_params:
                a_param = after_params[pname]
                b_def = b_param.get("default")
                a_def = a_param.get("default")
                if b_def != a_def and (b_def is not None or a_def is not None):
                    facts.append(
                        CodeFact(
                            fact_id=f"default-chg-{len(facts)+1}",
                            language="python",
                            path=path,
                            qualified_name=qname,
                            symbol=after_sig.name,
                            member=pname,
                            kind="default_changed",
                            before=str(b_def),
                            after=str(a_def),
                            line_before=before_sig.line_start,
                            line_after=after_sig.line_start,
                            source_change_id=change_id,
                            static_confidence="high",
                        )
                    )

        # Check removed parameters
        for pname in before_params:
            if pname not in after_params:
                facts.append(
                    CodeFact(
                        fact_id=f"param-rem-{len(facts)+1}",
                        language="python",
                        path=path,
                        qualified_name=qname,
                        symbol=after_sig.name,
                        member=pname,
                        kind="parameter_removed",
                        before=pname,
                        line_before=before_sig.line_start,
                        line_after=after_sig.line_start,
                        source_change_id=change_id,
                        static_confidence="high",
                    )
                )

        # Check added parameters
        for pname in after_params:
            if pname not in before_params:
                facts.append(
                    CodeFact(
                        fact_id=f"param-add-{len(facts)+1}",
                        language="python",
                        path=path,
                        qualified_name=qname,
                        symbol=after_sig.name,
                        member=pname,
                        kind="parameter_added",
                        after=pname,
                        line_before=before_sig.line_start,
                        line_after=after_sig.line_start,
                        source_change_id=change_id,
                        static_confidence="high",
                    )
                )

    # Added functions
    for qname, after_sig in after_facts.functions.items():
        if qname not in before_facts.functions:
            facts.append(
                CodeFact(
                    fact_id=f"func-add-{len(facts)+1}",
                    language="python",
                    path=path,
                    qualified_name=qname,
                    symbol=after_sig.name,
                    kind="function_added",
                    after=after_sig.name,
                    line_after=after_sig.line_start,
                    source_change_id=change_id,
                    static_confidence="high",
                )
            )

    # 2. Compare Constants
    for cname, (b_val, b_line) in before_facts.constants.items():
        if cname in after_facts.constants:
            a_val, a_line = after_facts.constants[cname]
            if b_val != a_val:
                facts.append(
                    CodeFact(
                        fact_id=f"const-chg-{len(facts)+1}",
                        language="python",
                        path=path,
                        qualified_name=cname,
                        symbol=cname,
                        member=cname,
                        kind="constant_changed",
                        before=b_val,
                        after=a_val,
                        line_before=b_line,
                        line_after=a_line,
                        source_change_id=change_id,
                        static_confidence="high",
                    )
                )

    # 3. Compare CLI Flags
    for flag, (b_def, b_line) in before_facts.cli_flags.items():
        if flag not in after_facts.cli_flags:
            facts.append(
                CodeFact(
                    fact_id=f"flag-chg-{len(facts)+1}",
                    language="python",
                    path=path,
                    symbol="argparse",
                    member=flag,
                    kind="config_flag_changed",
                    before=flag,
                    after=None,
                    line_before=b_line,
                    source_change_id=change_id,
                    static_confidence="high",
                )
            )
        else:
            a_def, a_line = after_facts.cli_flags[flag]
            if b_def != a_def:
                facts.append(
                    CodeFact(
                        fact_id=f"flag-chg-{len(facts)+1}",
                        language="python",
                        path=path,
                        symbol="argparse",
                        member=flag,
                        kind="config_flag_changed",
                        before=b_def,
                        after=a_def,
                        line_before=b_line,
                        line_after=a_line,
                        source_change_id=change_id,
                        static_confidence="high",
                    )
                )

    return facts
