import ast

from .unused_import import UnusedImportChecker
from .unreachable_code import UnreachableCodeChecker
from .dangerous_default import DangerousDefaultValueChecker
from .pointless_statement import PointlessStatementChecker
from .string_statement import StringStatementChecker
from .expression_not_assigned import ExpressionNotAssignedChecker
from .line_style import LineLengthAndTrailingWhitespaceChecker
from .statement import StatementChecker
from .indentation import IndentationChecker
from .file_structure import FileStructureChecker
from .missing_docstring import MissingDocstringChecker
from .unused_arg import UnusedArgumentChecker
from .attr_defined_outside import AttributeDefinedOutsideInitChecker
from .f_string import ConsiderUsingFStringChecker


class SimpleChecker:
    def __init__(self, code):
        self.tree = ast.parse(code)
        self.checkers = self.load_checkers()
        self.code = code

    def load_checkers(self):
        checkers = [
            UnusedImportChecker(),
            UnreachableCodeChecker(),
            DangerousDefaultValueChecker(),
            LineLengthAndTrailingWhitespaceChecker(),
            StatementChecker(),
            IndentationChecker(),
            MissingDocstringChecker(),
            UnusedArgumentChecker(),
            AttributeDefinedOutsideInitChecker(),
            ConsiderUsingFStringChecker(),
            # PointlessStatementChecker(),
            # StringStatementChecker(),
            # ExpressionNotAssignedChecker(),
            # FileStructureChecker(),
        ]
        return checkers

    def check(self):
        errors = []
        for checker in self.checkers:
            errors.extend(checker.check(self.tree))
        return errors
