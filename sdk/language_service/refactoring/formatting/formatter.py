from sdk.language_service.analysis.transformations.models import TransformationPlan

class ASTFormatter:
    """
    AST-based pretty printing integrated into the transformation pipeline.
    Replaces token-based 'lala fmt'.
    """
    def format_document(self, uri: str) -> TransformationPlan:
        return TransformationPlan("Format Document via AST")
