from typing import List, Dict
from sdk.language_service.providers.framework import CompletionProvider, LanguageRequestContext

class NamespaceProvider(CompletionProvider):
    def provide(self, context: LanguageRequestContext) -> List[Dict]:
        # Expose the lala namespace root
        return [{"label": "lala", "kind": 9, "detail": "Lala Standard Library"}]

class MemberProvider(CompletionProvider):
    def provide(self, context: LanguageRequestContext) -> List[Dict]:
        # Expose members of the lala namespace
        return [
            {"label": "print", "kind": 3, "detail": "lala.print()"},
            {"label": "math", "kind": 9, "detail": "lala.math"},
            {"label": "graphics", "kind": 9, "detail": "lala.graphics"},
        ]

class CompletionAggregator(CompletionProvider):
    def __init__(self):
        self.contributors = [
            NamespaceProvider(),
            MemberProvider()
        ]
        
    def provide(self, context: LanguageRequestContext) -> List[Dict]:
        results = []
        for contributor in self.contributors:
            results.extend(contributor.provide(context))
        return results
