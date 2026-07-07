from sdk.language_service.analysis.transformations.models import TransformationPlan

class ExtractMethodEngine:
    """
    Phase A: Staged implementation defining boundaries, parameters, and emitting the TransformationPlan.
    """
    def extract(self, uri: str, start_line: int, end_line: int) -> TransformationPlan:
        return TransformationPlan("Extract Method Phase A")
