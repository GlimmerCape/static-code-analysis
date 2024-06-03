import ast
from .checker import get_line_content


class UnusedArgumentChecker:
    def check(self, tree):
        errors = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                arg_names = {arg.arg for arg in node.args.args}
                used_names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
                unused_args = arg_names - used_names
                for arg in unused_args:
                    line_content = get_line_content(tree, node.lineno)
                    errors.append(f"RСтрока {node.lineno}: Неиспользованный аргумент'{arg}'.\n\t{line_content}")
        return errors
