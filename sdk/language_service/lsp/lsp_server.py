from sdk.language_service.service.service import LanguageService
import json
import sys

class LSPServer:
    def __init__(self, workspace):
        # The workspace is injected; LSP does not own it.
        self.service = LanguageService(workspace)

    def handle_request(self, method: str, params: dict) -> dict:
        if method == "initialize":
            return {
                "capabilities": {
                    "textDocumentSync": 1,
                    "completionProvider": {"triggerCharacters": ["."]},
                    "hoverProvider": True,
                    "semanticTokensProvider": {
                        "legend": {
                            "tokenTypes": ["namespace", "keyword", "type", "function", "variable", "string", "number"],
                            "tokenModifiers": []
                        }
                    }
                }
            }
        
        elif method == "textDocument/didChange":
            uri = params["textDocument"]["uri"]
            content = params["contentChanges"][0]["text"]
            version = params["textDocument"]["version"]
            # Trigger update via the scheduler/workspace (simplified here)
            self.service.workspace.document_manager.update(uri, content, version)
            return None
            
        elif method == "textDocument/completion":
            uri = params["textDocument"]["uri"]
            pos = params["position"]
            return {"items": self.service.completion(uri, pos["line"], pos["character"])}
            
        elif method == "textDocument/hover":
            uri = params["textDocument"]["uri"]
            pos = params["position"]
            return self.service.hover(uri, pos["line"], pos["character"])
            
        return None
