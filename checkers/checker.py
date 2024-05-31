class LineContentSingleton:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, tree="", code=""):
        if self._initialized:
            return
        self.tree = tree
        self.source_lines = code.split('\n')
        self._initialized = True

    def get_line_content(self, lineno):
        if lineno - 1 < len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return "<source not available>"


def get_line_content(module, lineno):
    line_content = LineContentSingleton()
    if lineno - 1 < len(line_content.source_lines):
        return line_content.source_lines[lineno - 1].strip()
    return "<source not available>"
