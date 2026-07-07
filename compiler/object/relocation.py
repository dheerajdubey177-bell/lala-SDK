from dataclasses import dataclass
from enum import Enum, auto

class RelocationKind(Enum):
    REL32 = auto() # 32-bit PC-relative relocation (e.g. CALL/JMP targets)
    ABS64 = auto() # 64-bit absolute relocation (e.g. pointers to data)

@dataclass
class Relocation:
    section: str # The section containing the bytes to patch
    offset: int # Offset within that section
    symbol_name: str # The symbol we are relocating against
    kind: RelocationKind
    addend: int
