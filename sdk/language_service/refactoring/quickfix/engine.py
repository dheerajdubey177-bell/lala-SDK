from typing import List
from sdk.language_service.analysis.transformations.models import TransformationPlan
from sdk.language_service.analysis.extraction.extraction import ExtractionDiagnostic

class CodeActionProvider:
    """
    Hook diagnostics to quick Transformations.
    """
    def provide(self, diagnostic: ExtractionDiagnostic) -> List[TransformationPlan]:
        # Stub: If diagnostic is "Unused variable", return "Remove variable" plan
        return []

class QuickFixEngine:
    def __init__(self):
        self.providers = [CodeActionProvider()]
        
    def get_fixes(self, diagnostic: ExtractionDiagnostic) -> List[TransformationPlan]:
        plans = []
        for provider in self.providers:
            plans.extend(provider.provide(diagnostic))
        return plans
