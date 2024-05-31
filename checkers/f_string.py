import ast
from .checker import get_line_content


class ConsiderUsingFStringChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Str):
                line_content = get_line_content(tree, node.lineno)
                errors.append(f"Строка {node.lineno}: Стоит использовать f-string для '{node.left.s}'.\n\t{line_content}")
        return errors
