class SymbolId:
    """
    An opaque internal identifier for a symbol.
    Consumers must never inspect this class directly; they only pass it to the NavigationEngine.
    """
    def __init__(self, internal_id: str):
        self._id = internal_id

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return isinstance(other, SymbolId) and self._id == other._id

class Resolver:
    """
    Translates a physical position in a document into an opaque SymbolId.
    Answers: 'What symbol is under this cursor?'
    """
    def __init__(self, workspace):
        self.workspace = workspace

    def resolve_at_position(self, uri: str, line: int, char: int) -> SymbolId | None:
        """
        Interrogates the compiler AST/SymbolIndex to determine the specific symbol at this location.
        Returns None if no symbol is found.
        """
        # Stub: Traverse AST or query SymbolIndex
        # Imagine finding a variable definition and hashing its unique scope location
        return SymbolId(f"{uri}:{line}:{char}")
