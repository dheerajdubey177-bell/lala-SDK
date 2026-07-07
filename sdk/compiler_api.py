from typing import Tuple, List, Optional, Dict
from sdk.project.model import Project

class DiagnosticsCategory:
    ERROR = "Error"
    WARNING = "Warning"
    STYLE = "Style"
    PERF = "Performance"
    SUGGESTION = "Suggestion"

class CompilerAPI:
    @staticmethod
    def compile(project: Project) -> Tuple[bool, Optional[bytes], List[str]]:
        if not project.source_files:
            return False, None, ["No source files found."]
            
        source = project.source_files[0].content
        
        from tests.framework.golden_tester import compile_to_asm
        try:
            asm, elf_bytes = compile_to_asm(source)
            if asm.startswith("ERROR:"):
                return False, None, [asm]
            return True, elf_bytes, []
        except Exception as e:
            return False, None, [str(e)]

    @staticmethod
    def check(project: Project) -> List[str]:
        """
        Runs static analysis on the project and returns a list of diagnostics.
        """
        # Stub: hook up to static analyzer
        from sdk.checker.checker import StaticChecker
        return StaticChecker().check(project)

    @staticmethod
    def format(project: Project) -> Dict[str, str]:
        """
        Returns a mapping of filepath to formatted source code.
        """
        # Stub: hook up to formatter
        from sdk.formatter.formatter import LalaFormatter
        results = {}
        for sf in project.source_files:
            results[str(sf.path)] = LalaFormatter().format(sf.content)
        return results
