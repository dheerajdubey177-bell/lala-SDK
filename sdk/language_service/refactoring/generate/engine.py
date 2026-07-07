from typing import List
from sdk.language_service.analysis.transformations.models import TransformationPlan

class GeneratorProvider:
    def generate(self, uri: str, line: int, char: int) -> List[TransformationPlan]:
        return []

class ConstructorGenerator(GeneratorProvider):
    def generate(self, uri: str, line: int, char: int) -> List[TransformationPlan]:
        return [TransformationPlan("Generate Constructor")]

class ToStringGenerator(GeneratorProvider):
    def generate(self, uri: str, line: int, char: int) -> List[TransformationPlan]:
        return [TransformationPlan("Generate ToString")]

class CodeGenerationEngine:
    """
    Educational languages benefit enormously from structural code generation.
    """
    def __init__(self):
        self.generators = [ConstructorGenerator(), ToStringGenerator()]
        
    def generate_options(self, uri: str, line: int, char: int) -> List[TransformationPlan]:
        plans = []
        for gen in self.generators:
            plans.extend(gen.generate(uri, line, char))
        return plans
