import ast
from .checker import get_line_content


class AttributeDefinedOutsideInitChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for method in node.body:
                    if isinstance(method, ast.FunctionDef) and method.name != '__init__':
                        for stmt in method.body:
                            if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Attribute):
                                line_content = get_line_content(tree, stmt.lineno)
                                errors.append(f"Строка {stmt.lineno}: Атрибут '{stmt.targets[0].attr}' определен за пределами __init__ функций.\n\t{line_content}")
        return errors
