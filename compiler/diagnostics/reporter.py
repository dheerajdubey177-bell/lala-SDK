from dataclasses import dataclass
from compiler.ast.base import Span
from .error_codes import ErrorCode, Severity

@dataclass
class Diagnostic:
    code: ErrorCode
    severity: Severity
    span: Span
    message: str
    suggestion: str | None = None
    explanation: str | None = None

    def __str__(self):
        result = f"[{self.code.value}] {self.severity.value}: {self.message}\n"
        result += f"  --> {self.span}\n"
        if self.suggestion:
            result += f"  Suggestion: {self.suggestion}\n"
        if self.explanation:
            result += f"  Explanation: {self.explanation}\n"
        return result

class DiagnosticReporter:
    def __init__(self):
        self.diagnostics: list[Diagnostic] = []

    def report(self, diagnostic: Diagnostic):
        self.diagnostics.append(diagnostic)

    def has_errors(self) -> bool:
        return any(d.severity == Severity.ERROR for d in self.diagnostics)

    def print_all(self):
        for d in self.diagnostics:
            print(d)
