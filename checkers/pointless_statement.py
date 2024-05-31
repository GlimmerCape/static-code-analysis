import ast
from .checker import get_line_content


class PointlessStatementChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and not isinstance(node.value, ast.Call):
                line_content = get_line_content(tree, node.lineno)
                errors.append(f"Строка {node.lineno}: Это строка ничего не делает.\n\t{line_content}")
        return errors
