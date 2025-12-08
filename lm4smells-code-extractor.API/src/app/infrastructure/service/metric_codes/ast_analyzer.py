import ast
from typing import Dict, List, Any, Tuple

class ASTAnalyzer:
    def count_parameters_from_source(self, source: str, filename: str) -> List[Dict[str, Any]]:
        tree = ast.parse(source, filename=filename)
        methods: List[Dict[str, Any]] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                positional = len(node.args.args)          # includes self/cls if present
                kwonly = len(node.args.kwonlyargs)
                vararg = 1 if node.args.vararg else 0     # *args
                varkw  = 1 if node.args.kwarg else 0      # **kwargs
                defaults = len(node.args.defaults)         # auxiliary info

                total = positional + kwonly + vararg + varkw

                methods.append({
                    "name": node.name,
                    "line": node.lineno,
                    "parameters": {
                        "total": total,
                        "positional": positional,
                        "positional_with_defaults": defaults,
                        "kwonly": kwonly,
                        "vararg": vararg,
                        "varkw": varkw,
                    },
                    "filename": filename,
                })

        return methods

    def count_parameters_from_sources(self, sources: List[str], filenames: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        results: Dict[str, List[Dict[str, Any]]] = {}
        for src, fname in zip(sources, filenames):
            results[fname] = self.count_parameters_from_source(src, fname)
        return results
    
    def calculate_loc_and_total(self, code_lines: List[str]) -> Tuple[int, int]:
        total_lines = len(code_lines)
        loc = sum(1 for line in code_lines if line.strip() and not line.strip().startswith("#"))
        return loc, total_lines

    # ---------- 🔽 NOVOS AUXILIARES REFEITOS 🔽 ----------

    def count_attributes(self, source: str, filename: str) -> Dict[str, Dict[str, int]]:

        tree = ast.parse(source, filename=filename)
        result: Dict[str, Dict[str, int]] = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total_attrs = 0
                for body_item in node.body:
                    if isinstance(body_item, ast.Assign):
                        total_attrs += len(body_item.targets)
                result[node.name] = {"total_attributes": total_attrs}

        return result

    def count_methods(self, source: str, filename: str) -> Dict[str, Dict[str, Any]]:

        tree = ast.parse(source, filename=filename)
        result: Dict[str, Dict[str, Any]] = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                result[node.name] = {
                    "total_methods": len(methods),
                    "start_line": node.lineno,
                }

        return result
    
    

    def count_class_loc(self, source: str, filename: str, start_line: int) -> int:

        lines = source.splitlines()
       # get the indentation of the class line
        indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
        loc = 0
        for i in range(start_line, len(lines)):
            line = lines[i]
            if line.strip() and not line.strip().startswith("#"):
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level and i > start_line:
                    break
                loc += 1
        return loc

    def calculate_dit(self, source: str, filename: str, class_name: str) -> int:

        tree = ast.parse(source, filename=filename)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return len(node.bases) if node.bases else 1
        return 1

    def parse_source(self, source: str, filename: str):

        tree = ast.parse(source, filename=filename)
        # add reference to 'parent' (required in Magic Number)
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        return tree

    def iter_numeric_literals(self, tree):
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
                yield float(n.value), n, getattr(n, "parent", None)
            elif (
                isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub)
                and isinstance(n.operand, ast.Constant)
                and isinstance(n.operand.value, (int, float))
            ):
                yield float(-n.operand.value), n, getattr(n, "parent", None)

    def is_constant_assignment(self, node) -> bool:
        p = node
        while p is not None and not isinstance(p, (ast.Assign, ast.AnnAssign, ast.arg)):
            p = getattr(p, "parent", None)

        if isinstance(p, ast.Assign):
            targets = [t.id for t in p.targets if isinstance(t, ast.Name)]
            return any(t.isupper() for t in targets)

        if isinstance(p, ast.AnnAssign) and isinstance(p.target, ast.Name):
            return p.target.id.isupper()

        return False

    def is_parameter_default(self, node) -> bool:
        p = node
        while p is not None and not isinstance(p, (ast.arg,)):
            p = getattr(p, "parent", None)
        return isinstance(p, ast.arg)


    def calculate_lcom(self, source: str, filename: str):
        tree = ast.parse(source, filename=filename)
        results = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                attributes = set()

                for method in methods:
                    for subnode in ast.walk(method):
                        if (
                            isinstance(subnode, ast.Attribute)
                            and isinstance(subnode.value, ast.Name)
                            and subnode.value.id == "self"
                        ):
                            attributes.add(subnode.attr)

                results[node.name] = (
                    0.0
                    if not methods or not attributes
                    else 1 - (len(attributes) / (len(methods) * len(attributes)))
                )

        return results


    def calculate_lwmc(self, source: str, filename: str):
        tree = ast.parse(source, filename=filename)
        results = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total_complexity = 0
                for method in [n for n in node.body if isinstance(n, ast.FunctionDef)]:
                    total_complexity += self.calculate_cyclomatic_complexity(method)
                results[node.name] = total_complexity

        return results
    
    def calculate_cyclomatic_complexity(self, node: ast.AST) -> int:

        complexity = 1  # starts at 1 by definition

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):  # multiple conditions in if/while
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1

        return complexity

