import ast
from .checker import get_line_content


class DangerousDefaultValueChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.defaults:
                    if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                        line_content = get_line_content(tree, node.lineno)
                        errors.append(f"EСтрока {node.lineno}: Опасное значение по умолчанию {ast.dump(arg)} у аргумента.\n\t{line_content}")
        return errors
