import ast
from .checker import get_line_content


class StringStatementChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                line_content = get_line_content(tree, node.lineno)
                errors.append(f"Строка {node.lineno}: У строчного выражения нет эффекта.\n\t{line_content}")
        return errors
