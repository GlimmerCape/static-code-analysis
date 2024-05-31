from checkers.basic_checker import SimpleChecker
from checkers.checker import LineContentSingleton


def lint(code):
    line_content = LineContentSingleton("", "")
    line_content.source_lines = code.split('\n')
    checker = SimpleChecker(code)
    return checker.check()
