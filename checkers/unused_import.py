import ast


class UnusedImportChecker:
    def check(self, tree):
        errors = []
        imported_names = set()
        used_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names.add(alias.name)
            elif isinstance(node, ast.Name):
                used_names.add(node.id)

        unused_imports = imported_names - used_names
        for name in unused_imports:
            errors.append(f"RНайден импортированный, но неиспользованный модуль: {name}")
        return errors
