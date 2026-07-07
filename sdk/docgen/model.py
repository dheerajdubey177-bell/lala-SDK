from dataclasses import dataclass
from typing import List

@dataclass
class DocNode:
    name: str
    description: str
    kind: str # e.g. "function", "module"

class DocGenerator:
    def generate(self, ast) -> List[DocNode]:
        """
        Traverses AST to produce the documentation model.
        """
        nodes = []
        # Stub: Traverse AST for docstrings
        return nodes
