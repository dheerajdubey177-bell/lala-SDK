class CompilerError:
    def __init__(self, code, message, line, column, length=1, hint=None):
        self.code = code
        self.message = message
        self.line = line
        self.column = column
        self.length = length
        self.hint = hint

class DiagnosticsReporter:
    def __init__(self, context):
        self.context = context
        self.errors = []
        self.warnings = []

    def error(self, code, message, line, column, length=1, hint=None):
        self.errors.append(CompilerError(code, message, line, column, length, hint))

    def warning(self, code, message, line, column, length=1, hint=None):
        self.warnings.append(CompilerError(code, message, line, column, length, hint))

    def has_errors(self):
        return len(self.errors) > 0

    def print_diagnostics(self):
        if self.has_errors():
            print(f"{len(self.errors)} errors found\n")
            
        lines = self.context.source_code.split('\n')
        
        for err in self.errors:
            print(f"{err.code}\n")
            print(f"{err.message}\n")
            
            if 0 < err.line <= len(lines):
                source_line = lines[err.line - 1]
                print(f"{err.line} │ {source_line}")
                
                # Print carets
                padding = len(str(err.line)) + 3 + err.column
                carets = "^" * max(1, err.length)
                print(" " * padding + carets)
            
            if err.hint:
                print(f"\n{err.hint}")
            print("\n" + "-"*40 + "\n")
