from typing import Dict, Set, List
from sdk.language_service.analysis.cfg.graph import ControlFlowGraph, BasicBlock
from sdk.language_service.analysis.references.resolver import SymbolId

class DefUseAnalysis:
    """
    Computes definition-use and use-definition chains.
    """
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.def_use: Dict[SymbolId, List[dict]] = {}
        self.use_def: Dict[SymbolId, List[dict]] = {}

class LiveVariablesAnalysis:
    """
    Computes Live-In and Live-Out sets for each BasicBlock.
    """
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.live_in: Dict[BasicBlock, Set[SymbolId]] = {}
        self.live_out: Dict[BasicBlock, Set[SymbolId]] = {}

class ReachingDefinitionsAnalysis:
    """
    Computes which definitions reach which blocks.
    """
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.reaching_in: Dict[BasicBlock, Set[dict]] = {}
        self.reaching_out: Dict[BasicBlock, Set[dict]] = {}
