import ast
from .checker import get_line_content


class LineLengthAndTrailingWhitespaceChecker:
    MAX_LINE_LENGTH = 80

    def check(self, module):
        errors = []
        for node in ast.walk(module):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                if len(node.value.s) > self.MAX_LINE_LENGTH:
                    line_content = get_line_content(module, node.lineno)
                    errors.append(f"CСтрока {node.lineno}: Слишком длинная строка ({len(node.value.s)}/{self.MAX_LINE_LENGTH})\n\t{line_content}")
                if node.value.s.rstrip() != node.value.s:
                    line_content = get_line_content(module, node.lineno)
                    errors.append(f"CСтрока {node.lineno}: Лишние пробелы в конце строки\n\t{line_content}")
        return errors
