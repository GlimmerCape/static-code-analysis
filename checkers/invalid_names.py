import ast
import re
from .checker import get_line_content

CLASS_NAME_RE = re.compile(r'^[A-Z][a-zA-Z0-9]+$')
CONST_NAME_RE = re.compile(r'^[A-Z][A-Z0-9_]*$')
VAR_FUNC_NAME_RE = re.compile(r'^[a-z_][a-z0-9_]*$')


class InvalidNameChecker:
    def check_class_name(self, node):
        if not CLASS_NAME_RE.match(node.name):
            line_content = get_line_content(node.lineno)
            return f"CСтрока {node.lineno}: Наименование класса не соответствует PEP8 '{node.name}'. Имя должно быть в формате PascalCase.\n\t{line_content}"

    def check_function_name(self, node):
        if not VAR_FUNC_NAME_RE.match(node.name):
            line_content = get_line_content(node.lineno)
            return f"CСтрока {node.lineno}: Неправильное имя метода/функции '{node.name}'. Имя должно быть в формате lower_case_with_underscores.\n\t{line_content}"

    def check_variable_name(self, node):
        if not VAR_FUNC_NAME_RE.match(node.id):
            line_content = get_line_content(node.lineno)
            return f"CСтрока {node.lineno}: Неправильное имя переменной '{node.id}'. Имя должно быть в формате lower_case_with_underscores.\n\t{line_content}"

    def check_constant_name(self, node):
        if not CONST_NAME_RE.match(node.id):
            line_content = get_line_content(node.lineno)
            return f"CСтрока {node.lineno}: Неправильное имя константы '{node.id}'. Имя должно быть в формате UPPER_CASE_WITH_UNDERSCORES.\n\t{line_content}"

    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                errors.append(self.check_class_name(node))
            elif isinstance(node, ast.FunctionDef):
                errors.append(self.check_function_name(node))
            elif isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    errors.append(self.check_variable_name(node))
            elif isinstance(node, ast.Assign):
                if isinstance(node.targets[0], ast.Name):
                    errors.append(self.check_constant_name(node.targets[0]))
        return errors
