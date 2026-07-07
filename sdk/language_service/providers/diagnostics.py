from typing import List, Dict
from sdk.language_service.providers.framework import DiagnosticsProvider, LanguageRequestContext

class SyntaxDiagnosticProvider(DiagnosticsProvider):
    def provide(self, context: LanguageRequestContext) -> List[Dict]:
        # Stub syntax checker
        return []
        
class SemanticDiagnosticProvider(DiagnosticsProvider):
    def provide(self, context: LanguageRequestContext) -> List[Dict]:
        # Stub semantic checker
        return []

class DiagnosticAggregator(DiagnosticsProvider):
    def __init__(self):
        self.contributors = [
            SyntaxDiagnosticProvider(),
            SemanticDiagnosticProvider()
        ]
        
    def provide(self, context: LanguageRequestContext) -> List[Dict]:
        results = []
        for contributor in self.contributors:
            results.extend(contributor.provide(context))
        return results
