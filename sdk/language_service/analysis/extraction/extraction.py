from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass
from sdk.language_service.analysis.references.resolver import SymbolId
from sdk.language_service.analysis.cfg.graph import Terminator

class ExtractionStatus(Enum):
    EXTRACTABLE = 1
    EXTRACTABLE_WITH_WARNINGS = 2
    REQUIRES_TRANSFORMATION = 3
    NOT_EXTRACTABLE = 4

@dataclass
class ExtractionDiagnostic:
    severity: str
    code: str
    message: str
    location: dict

@dataclass
class SelectionAnalysis:
    """
    Answers whether an AST selection is structurally valid and complete.
    """
    is_valid: bool
    nodes: List[object] # AST nodes
    diagnostics: List[ExtractionDiagnostic]

@dataclass
class ExtractionAnalysis:
    """
    The fully computed semantic metadata required for extraction.
    Contains absolutely no code modifications or textual edits.
    """
    selection: SelectionAnalysis
    entry_symbols: List[SymbolId]
    exit_symbols: List[SymbolId]
    captured_symbols: List[SymbolId]
    referenced_types: List[SymbolId]
    called_functions: List[SymbolId]
    required_imports: List[str]
    control_exits: List[Terminator]
    diagnostics: List[ExtractionDiagnostic]
    status: ExtractionStatus

class SelectionAnalyzer:
    """
    Evaluates AST boundaries for a given textual selection range.
    """
    def analyze(self, uri: str, start_line: int, end_line: int) -> SelectionAnalysis:
        # Stub: verify full statement coverage, etc.
        return SelectionAnalysis(is_valid=True, nodes=[], diagnostics=[])

class ExtractionAnalyzer:
    """
    Consumes SelectionAnalysis, CFG, and DataFlow to produce the semantic ExtractionAnalysis.
    """
    def analyze(self, selection: SelectionAnalysis) -> ExtractionAnalysis:
        # Stub: perform live-in, live-out, and exit computations
        return ExtractionAnalysis(
            selection=selection,
            entry_symbols=[],
            exit_symbols=[],
            captured_symbols=[],
            referenced_types=[],
            called_functions=[],
            required_imports=[],
            control_exits=[],
            diagnostics=[],
            status=ExtractionStatus.EXTRACTABLE
        )
