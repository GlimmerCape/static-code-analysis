import ast
from .checker import get_line_content


class ExpressionNotAssignedChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and not isinstance(node.value, ast.Call):
                line_content = get_line_content(tree, node.lineno)
                errors.append(f"EСтрока {node.lineno}: Выражение {ast.dump(node.value)} не присваивается ни к какой перменной.\n\t{line_content}")
        return errors
