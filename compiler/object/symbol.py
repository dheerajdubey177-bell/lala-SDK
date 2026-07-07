from dataclasses import dataclass
from enum import Enum, auto

class SymbolKind(Enum):
    FUNC = auto()
    OBJECT = auto()
    NOTYPE = auto()

class SymbolBinding(Enum):
    LOCAL = auto()
    GLOBAL = auto()

@dataclass
class Symbol:
    name: str
    kind: SymbolKind
    binding: SymbolBinding
    section: str | None # None if external/undefined
    offset: int
    size: int
