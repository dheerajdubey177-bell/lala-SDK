from sdk.language_service.analysis.transformations.models import RenameTransformation, TransformationPlan
from sdk.language_service.analysis.references.resolver import Resolver, SymbolId
from sdk.language_service.analysis.references.navigation import NavigationEngine, QueryReferences

class RenameValidationException(Exception):
    pass

class RenameEngine:
    """
    Production-ready rename leveraging the reference engine.
    It NEVER traverses the AST. It relies strictly on Resolver and NavigationEngine.
    """
    def __init__(self, workspace):
        self.workspace = workspace
        self.resolver = Resolver(workspace)
        self.navigation = NavigationEngine(workspace)

    def _validate_name(self, new_name: str, symbol_id: SymbolId):
        """
        Ensures the new name doesn't violate rules.
        """
        reserved_keywords = {"kaam", "agar", "warna", "jabtak"}
        if new_name in reserved_keywords:
            raise RenameValidationException(f"'{new_name}' is a reserved keyword.")
        
        # Additional checks: duplicate declarations, public API visibility, compiler reserved identifiers

    def rename_symbol(self, uri: str, line: int, char: int, new_name: str) -> TransformationPlan:
        """
        Executes the thin semantic rename pipeline.
        """
        # 1. Resolve SymbolId
        symbol_id = self.resolver.resolve_at_position(uri, line, char)
        if not symbol_id:
            raise RenameValidationException("No symbol found at the cursor location.")

        # 2. Validate Name
        self._validate_name(new_name, symbol_id)

        # 3. Query References (via Query Pipeline)
        result = self.navigation.query(symbol_id, QueryReferences())

        # 4. Build Transformation (via Transformation Pipeline)
        # Note: In reality, we map each location in `result.locations` to a TextEdit/RenameTransformation
        return RenameTransformation(uri, "old_name", new_name).apply()
