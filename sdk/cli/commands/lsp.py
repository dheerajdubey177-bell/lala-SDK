import sys
import argparse
from pathlib import Path
from sdk.cli.command import Command
from sdk.language_service.workspace.workspace import WorkspaceBuilder
from sdk.language_service.lsp.lsp_server import LSPServer
import json

class LspCommand(Command):
    @property
    def name(self) -> str:
        return "lsp"

    @property
    def help(self) -> str:
        return "Launch the Language Server Protocol (LSP) backend"

    def execute(self, args: argparse.Namespace):
        print("Lala Language Server initialized.", file=sys.stderr)
        root_uri = "file://" + str(Path.cwd().absolute().as_posix())
        workspace = WorkspaceBuilder.build(root_uri)
        server = LSPServer(workspace)
        
        # Simple JSON-RPC read loop stub for stdio
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                # Very naive JSON-RPC parsing for this stub
                if line.startswith("Content-Length:"):
                    length = int(line.split(":")[1].strip())
                    sys.stdin.readline() # Read \r\n
                    payload = sys.stdin.read(length)
                    data = json.loads(payload)
                    
                    method = data.get("method")
                    params = data.get("params", {})
                    response_id = data.get("id")
                    
                    result = server.handle_request(method, params)
                    
                    if response_id is not None:
                        response = {
                            "jsonrpc": "2.0",
                            "id": response_id,
                            "result": result
                        }
                        response_str = json.dumps(response)
                        sys.stdout.write(f"Content-Length: {len(response_str)}\r\n\r\n{response_str}")
                        sys.stdout.flush()
                        
            except Exception as e:
                print(f"LSP Error: {e}", file=sys.stderr)
                break

COMMAND = LspCommand()
