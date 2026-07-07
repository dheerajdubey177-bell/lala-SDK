from dataclasses import dataclass, field
from .section import Section
from .symbol import Symbol
from .relocation import Relocation

@dataclass
class ObjectFile:
    sections: list[Section] = field(default_factory=list)
    symbols: list[Symbol] = field(default_factory=list)
    relocations: list[Relocation] = field(default_factory=list)
