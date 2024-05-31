import ast
from .checker import get_line_content


class IndentationChecker:
    def check(self, module):
        errors = []
        expected_indent = None
        for node in ast.walk(module):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                line_indent = len(node.value.s) - len(node.value.s.lstrip())
                if expected_indent is None:
                    line_content = get_line_content(module, node.lineno)
                    expected_indent = line_indent
                elif line_indent != expected_indent:
                    line_content = get_line_content(module, node.lineno)
                    errors.append(f"Строка {node.lineno}: Некорректная индентация. Найдено {line_indent} пробелов, ожидалось {expected_indent}\n\t{line_content}")
        return errors
