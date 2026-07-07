from typing import List, Dict, Optional
from sdk.language_service.workspace.workspace import Workspace
from sdk.language_service.providers.framework import LanguageRequestContext
from sdk.language_service.providers.completion import CompletionAggregator
from sdk.language_service.providers.hover import MarkdownHoverProvider
from sdk.language_service.providers.diagnostics import DiagnosticAggregator

class LanguageService:
    """
    Stateless orchestration layer.
    Owns zero compiler state. All state is maintained in the Workspace.
    """
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.completion_provider = CompletionAggregator()
        self.hover_provider = MarkdownHoverProvider()
        self.diagnostics_provider = DiagnosticAggregator()

    def _create_context(self, uri: str, line: int = 0, character: int = 0) -> LanguageRequestContext:
        """Constructs an immutable request context snapshot for pure providers."""
        snapshot = self.workspace.document_manager.snapshot(uri)
        session = self.workspace.snapshot()
        return LanguageRequestContext(
            workspace=session,
            document=snapshot,
            position={"line": line, "character": character}
        )

    def completion(self, uri: str, line: int, character: int) -> List[Dict]:
        context = self._create_context(uri, line, character)
        if not context.document:
            return []
        return self.completion_provider.provide(context)

    def hover(self, uri: str, line: int, character: int) -> Optional[Dict]:
        context = self._create_context(uri, line, character)
        if not context.document:
            return None
        return self.hover_provider.provide(context)

    def diagnostics(self, uri: str) -> List[Dict]:
        context = self._create_context(uri)
        if not context.document:
            return []
        return self.diagnostics_provider.provide(context)
