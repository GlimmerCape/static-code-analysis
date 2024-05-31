import unittest
from main import lint


class TestSimpleChecker(unittest.TestCase):
    def test_check_unused_import(self):
        code = "import os\n\nprint('Hello')"
        errors = lint(code)
        self.assertIn("Unused import detected: os", errors)

    def test_check_unreachable_code(self):
        code = """
def example():
    return
    print('This is unreachable')
"""
        errors = lint(code)
        self.assertIn("Line 4: Unreachable code detected.", errors)

    def test_check_dangerous_default_value(self):
        code = """
def example(a=[]):
    pass
"""
        errors = lint(code)
        self.assertIn("Line 2: Dangerous default value List() as argument.", errors)

    def test_check_pointless_statement(self):
        code = """
42
        """
        errors = lint(code)
        self.assertIn("Line 2: Statement seems to have no effect.", errors)

    def test_check_string_statement(self):
        code = """
'This is a string statement'
        """
        errors = lint(code)
        self.assertIn("Line 2: String statement has no effect.", errors)

    def test_check_expression_not_assigned(self):
        code = """
3 + 4
        """
        errors = lint(code)
        self.assertIn("Line 2: Expression BinOp(left=Num(n=3), op=Add(), right=Num(n=4)) is assigned to nothing.", errors)

    def test_check_line_too_long(self):
        code = "a" * 81
        errors = lint(code)
        self.assertIn("Line 1: Line too long (81/80)", errors)

    def test_check_trailing_whitespace(self):
        code = "print('hello') \n"
        errors = lint(code)
        self.assertIn("Line 1: Trailing whitespace", errors[0])

    def test_check_final_newline(self):
        code = "print('hello')"
        errors = lint(code)
        self.assertIn("Final newline missing", errors[0])

    def test_check_trailing_newlines(self):
        code = "print('hello')\n\n"
        errors = lint(code)
        self.assertIn("Trailing newlines", errors[0])

    def test_check_bad_indentation(self):
        code = "def func():\n  print('hello')\n    print('world')"
        errors = lint(code)
        self.assertIn("Line 3: Bad indentation. Found 4 spaces, expected 2", errors[0])

    def test_check_unnecessary_semicolon(self):
        code = "print('hello');"
        errors = lint(code)
        self.assertIn("Line 1: Unnecessary semicolon", errors[0])

    def test_check_multiple_statements(self):
        code = "print('hello'); print('world')"
        errors = lint(code)
        self.assertIn("Line 1: More than one statement on a single line", errors[0])

    def test_check_unnecessary_parens(self):
        code = "if (True): pass"
        errors = lint(code)
        self.assertIn("Line 1: Unnecessary parens after if", errors[0])


if __name__ == "__main__":
    unittest.main()
