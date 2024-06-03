import ast
from .checker import get_line_content


class StatementChecker:
    def check(self, module):
        errors = []
        for node in ast.walk(module):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                if ';' in node.value.s:
                    statements = node.value.s.split(';')
                    if len(statements) > 1:
                        line_content = get_line_content(module, node.lineno)
                        errors.append(f"RСтрока {node.lineno}: Несколько выражений на одной строке\n\t{line_content}")
            # elif isinstance(node, (ast.If, ast.For, ast.While, ast.With)) and isinstance(node.test, ast.Tuple):
            #     errors.append(f"Line {node.lineno}: Unnecessary parens after {node.__class__.__name__.lower()}")
        return errors
