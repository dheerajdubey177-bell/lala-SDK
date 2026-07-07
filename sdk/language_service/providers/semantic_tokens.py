from typing import List, Dict
from sdk.language_service.providers.framework import SemanticTokenProvider, LanguageRequestContext

class LalaSemanticTokenProvider(SemanticTokenProvider):
    def provide(self, context: LanguageRequestContext) -> List[int]:
        """
        Generates semantic tokens (line, char, length, tokenType, tokenModifiers).
        """
        # Stub
        return []
