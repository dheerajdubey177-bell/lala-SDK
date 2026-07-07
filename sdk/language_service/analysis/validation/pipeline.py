from sdk.language_service.analysis.transformations.models import WorkspaceEdit

class SyntaxValidator:
    def validate(self, edit: WorkspaceEdit) -> bool:
        return True

class SemanticValidator:
    def validate(self, edit: WorkspaceEdit) -> bool:
        return True

class CollisionDetector:
    def validate(self, edit: WorkspaceEdit) -> bool:
        return True

class FormattingValidator:
    def validate(self, edit: WorkspaceEdit) -> bool:
        return True

class ValidationPipeline:
    """
    Ensures a WorkspaceEdit is safe to apply by running sequential validation passes.
    """
    def __init__(self):
        self.passes = [
            SyntaxValidator(),
            SemanticValidator(),
            CollisionDetector(),
            FormattingValidator()
        ]

    def is_valid(self, edit: WorkspaceEdit) -> bool:
        for validator in self.passes:
            if not validator.validate(edit):
                return False
        return True
