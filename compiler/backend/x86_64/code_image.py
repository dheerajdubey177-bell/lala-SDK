from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List
from .machine_ir import MachineInstruction

class FixupKind(Enum):
    REL32 = auto() # 32-bit relative offset (used in JMP, CALL, Jcc)
    
@dataclass
class Fixup:
    offset: int # Byte offset relative to the start of the CodeImage
    kind: FixupKind
    target_label: str # The block or function name we want to jump to

@dataclass
class EncodedInstruction:
    machine_instruction: MachineInstruction
    bytes_data: bytes
    offset: int # Offset relative to start of CodeImage
    length: int
    fixups: List[Fixup] = field(default_factory=list)
    
@dataclass
class EncodedBlock:
    name: str
    instructions: List[EncodedInstruction]
    bytes_data: bytes
    offset: int
    length: int

@dataclass
class EncodedFunction:
    name: str
    blocks: List[EncodedBlock]
    bytes_data: bytes
    offset: int
    length: int

@dataclass
class CodeImage:
    functions: List[EncodedFunction]
    bytes_data: bytes
    fixups: List[Fixup] = field(default_factory=list)
