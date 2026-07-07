from typing import Dict, Any
from dataclasses import dataclass
from sdk.language_service.workspace.workspace import WorkspaceSession
from sdk.language_service.workspace.document import DocumentSnapshot

@dataclass
class LanguageRequestContext:
    """
    The immutable context passed to every pure provider.
    Carries the frozen workspace state and request constraints.
    """
    workspace: WorkspaceSession
    document: DocumentSnapshot
    position: dict # e.g. {"line": 0, "character": 0}
    cancellation_token: object = None
    deadline: float = 0.0
    capabilities: dict = None
    user_settings: dict = None

class Provider:
    """
    Base contract for all language feature providers.
    Providers must be pure: input -> workspace -> result.
    They never mutate the workspace.
    """
    pass

class CompletionProvider(Provider):
    def provide(self, context: LanguageRequestContext) -> list:
        raise NotImplementedError

class HoverProvider(Provider):
    def provide(self, context: LanguageRequestContext) -> dict:
        raise NotImplementedError

class DiagnosticsProvider(Provider):
    def provide(self, context: LanguageRequestContext) -> list:
        raise NotImplementedError

class SemanticTokenProvider(Provider):
    def provide(self, context: LanguageRequestContext) -> list:
        raise NotImplementedError
