from sdk.language_service.service.service import LanguageService
from sdk.language_service.workspace.workspace import WorkspaceBuilder

class PlaygroundServer:
    def __init__(self):
        # We start with a mock root for the playground memory-only files
        self.workspace = WorkspaceBuilder.build("file:///playground")
        self.service = LanguageService(self.workspace)

    def handle_request(self, method: str, payload: dict) -> dict:
        """
        Translates HTTP/WebSocket REST payloads to LanguageService.
        """
        if method == "update_and_diagnose":
            self.workspace.document_manager.update("file:///playground/main.lala", payload["code"], 1)
            return {"diagnostics": self.service.diagnostics("file:///playground/main.lala")}
            
        return {"error": "Method not found"}
