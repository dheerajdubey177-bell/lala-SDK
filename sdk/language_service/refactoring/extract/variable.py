from sdk.language_service.analysis.transformations.models import TransformationPlan, CompositeTransformation
from sdk.language_service.analysis.references.resolver import Resolver
from sdk.language_service.analysis.references.navigation import NavigationEngine

class ExtractVariableEngine:
    """
    Evaluates an expression and extracts it into a local variable.
    Pipeline: Expression -> Type -> Scope -> Insert Variable -> Replace Expression
    """
    def __init__(self, workspace):
        self.workspace = workspace
        self.resolver = Resolver(workspace)

    def extract(self, uri: str, start_line: int, start_char: int, end_line: int, end_char: int, var_name: str = "extracted_var") -> TransformationPlan:
        # 1. Validate Selection (simulate finding the exact AST node for the expression)
        # 2. Determine insertion point (just above the statement containing the expression)
        # 3. Create two edits:
        #    a. Insert `var_name = <expression>`
        #    b. Replace `<expression>` with `var_name`
        
        # We simulate the composite transformation plan
        return CompositeTransformation(
            description=f"Extract variable '{var_name}'",
            transformations=[] # In reality, InsertTransformation + ReplaceTransformation
        ).apply()
