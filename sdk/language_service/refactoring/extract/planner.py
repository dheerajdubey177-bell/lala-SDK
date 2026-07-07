from typing import List
from dataclasses import dataclass
from sdk.language_service.analysis.extraction.extraction import ExtractionAnalysis
from sdk.language_service.analysis.transformations.models import TransformationPlan, CompositeTransformation

@dataclass
class ExtractionPlan:
    """
    Semantic blueprint for the refactoring.
    """
    new_function_name: str
    parameters: List[str]
    return_values: List[str]
    insertion_location: dict
    call_site_replacement: str

class ParameterStrategy:
    def determine(self, analysis: ExtractionAnalysis) -> List[str]:
        # Stub: order parameters by usage or name
        return [str(sym) for sym in analysis.entry_symbols]

class ReturnStrategy:
    def determine(self, analysis: ExtractionAnalysis) -> List[str]:
        # Stub: handle single return, multiple returns, or mutations
        return [str(sym) for sym in analysis.exit_symbols]

class InsertionStrategy:
    def determine(self, analysis: ExtractionAnalysis) -> dict:
        # Stub: find nearest scope boundary to insert the extracted function
        return {"line": 0, "char": 0}

class ExtractionPlanner:
    """
    Consumes ExtractionAnalysis to make semantic planning decisions.
    Produces an ExtractionPlan, which converts into a CompositeTransformation.
    """
    def __init__(self):
        self.param_strategy = ParameterStrategy()
        self.return_strategy = ReturnStrategy()
        self.insertion_strategy = InsertionStrategy()

    def plan(self, analysis: ExtractionAnalysis, new_name: str = "extracted_function") -> ExtractionPlan:
        return ExtractionPlan(
            new_function_name=new_name,
            parameters=self.param_strategy.determine(analysis),
            return_values=self.return_strategy.determine(analysis),
            insertion_location=self.insertion_strategy.determine(analysis),
            call_site_replacement=f"{new_name}()" # Highly simplified
        )
        
    def to_transformation(self, plan: ExtractionPlan) -> TransformationPlan:
        """
        Translates the plan into a semantic TransformationPlan (composed of smaller transformations).
        """
        # Note: We would instantiate InsertTransformation and ReplaceTransformation here.
        # Returning a stub CompositeTransformation
        return CompositeTransformation(
            description=f"Extract Method {plan.new_function_name}",
            transformations=[]
        ).apply()
