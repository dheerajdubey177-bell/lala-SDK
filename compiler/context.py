from .semantics.symbols import Scope
from .session import CompilerSession

class CompilationContext:
    def __init__(self, session: CompilerSession, file: str):
        self.session = session
        self.file = file
        self.ast = None
        
        # Scopes and Symbols
        self.global_scope = Scope(name="Global")
        self.node_scopes = {}
        self.resolved_symbols = {}
        
        # Types
        self.node_types = {} # Maps AST Expression node IDs to their resolved Type objects
        
        # Bindings (to be collapsed into Bound AST)
        self.bound_calls = {} # Maps AST node ID to IntrinsicID or RuntimeID

    @property
    def diagnostics(self):
        return self.session.diagnostics
        
    @property
    def type_registry(self):
        return self.session.type_registry
