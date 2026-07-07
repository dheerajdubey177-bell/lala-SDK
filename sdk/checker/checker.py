from sdk.project.model import Project
from typing import List

class StaticChecker:
    def check(self, project: Project) -> List[str]:
        """
        Runs static analysis across the project and emits diagnostics.
        """
        diagnostics = []
        # Stub: Traverse AST or HIR for warnings
        # Examples of future diagnostics:
        # diagnostics.append("Warning: Unused variable 'x'")
        # diagnostics.append("Style: Function 'DoSomething' should be camelCase 'doSomething'")
        return diagnostics
