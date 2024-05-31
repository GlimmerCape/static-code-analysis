import ast


class FileStructureChecker:
    MAX_LINES = 200

    def check(self, module):
        errors = []
        # line_count = len(module.body)
        # if line_count > self.MAX_LINES:
            # errors.append(f"Too many lines in module ({line_count}/{self.MAX_LINES})")
        # if not module.body or not isinstance(module.body[-1], ast.Expr) and module.body[-1].value.s[-1] != '\n':
            # errors.append("Final newline missing")
        return errors
