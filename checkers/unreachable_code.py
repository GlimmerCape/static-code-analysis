import ast
from .checker import get_line_content


class UnreachableCodeChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for body_node in node.body:
                    if isinstance(body_node, (ast.Return, ast.Raise)):
                        for unreachable in node.body[node.body.index(body_node) + 1:]:
                            line_content = get_line_content(tree, node.lineno)
                            errors.append(f"Строка {unreachable.lineno}: Недостижимый код.\n\t{line_content}")
                        break
        return errors
