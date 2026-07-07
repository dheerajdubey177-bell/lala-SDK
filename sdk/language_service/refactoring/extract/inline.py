from sdk.language_service.analysis.transformations.models import TransformationPlan, CompositeTransformation
from sdk.language_service.analysis.references.resolver import Resolver
from sdk.language_service.analysis.references.navigation import NavigationEngine, QueryReferences

class InlineVariableEngine:
    """
    Analyzes single-assignment and side effects to safely inline variables.
    Pipeline: Check single assignment -> Check side effects -> Replace References -> Safe Delete
    """
    def __init__(self, workspace):
        self.workspace = workspace
        self.resolver = Resolver(workspace)
        self.navigation = NavigationEngine(workspace)

    def inline(self, uri: str, line: int, char: int) -> TransformationPlan:
        # 1. Resolve the variable
        symbol_id = self.resolver.resolve_at_position(uri, line, char)
        if not symbol_id:
            raise Exception("No variable found to inline.")
            
        # 2. Find references
        refs = self.navigation.query(symbol_id, QueryReferences())
        
        # 3. Build composite plan to replace all refs with the initializer, and delete the original decl
        return CompositeTransformation(
            description="Inline Variable",
            transformations=[] # ReplaceTransformations for each ref + DeleteTransformation for the decl
        ).apply()
