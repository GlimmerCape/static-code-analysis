class SimpleReporter:
    def report(self, errors):
        for error in errors:
            print(f"Error: {error}")


def main(code):
    from main import lint
    reporter = SimpleReporter()
    errors = lint(code)
    reporter.report(errors)
