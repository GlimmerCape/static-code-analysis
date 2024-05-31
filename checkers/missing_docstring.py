import ast
from .checker import get_line_content


class MissingDocstringChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def check(self, tree):
        errors = []
        if not ast.get_docstring(tree):
            line_content = get_line_content(tree, 1)
            errors.append(f"Строка 1: У модуля нет строки с документацией.\n\t{line_content}")
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    line_content = get_line_content(tree, node.lineno)
                    errors.append(f"Строка {node.lineno}: У функции '{node.name}' нет строки с документацией.\n\t{line_content}")
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    line_content = get_line_content(tree, node.lineno)
                    errors.append(f"Строка {node.lineno}: У класса '{node.name}' нет строки с документацией.\n\t{line_content}")
        return errors
