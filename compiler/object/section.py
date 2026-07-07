from dataclasses import dataclass
from enum import Enum, auto

class SectionFlags(Enum):
    ALLOC = auto()
    EXEC = auto()
    WRITE = auto()

@dataclass
class Section:
    name: str
    flags: list[SectionFlags]
    alignment: int
    bytes_data: bytes
