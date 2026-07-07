from dataclasses import dataclass
from typing import Union
from .registers import X86Register
from .addressing import Address
from .opcodes import Opcode

# Operands
@dataclass(frozen=True)
class Immediate:
    value: int
    
    def __str__(self):
        return str(self.value)

@dataclass(frozen=True)
class MemoryOperand:
    address: Address
    
    def __str__(self):
        # We usually specify the size e.g. QWORD PTR but for now keeping it simple
        return str(self.address)

@dataclass(frozen=True)
class LabelOperand:
    name: str
    
    def __str__(self):
        return self.name

# A MachineOperand can be a Register, Immediate, Memory, or Label
MachineOperand = Union[X86Register, Immediate, MemoryOperand, LabelOperand]

@dataclass
class MachineInstruction:
    opcode: Opcode
    operands: list[MachineOperand]
    comment: str = ""
    
    def __str__(self):
        ops = ", ".join(str(op) for op in self.operands)
        s = f"{self.opcode.name} {ops}" if ops else self.opcode.name
        if self.comment:
            s += f" # {self.comment}"
        return s

@dataclass
class MachineBlock:
    name: str
    instructions: list[MachineInstruction]
    
@dataclass
class MachineFunction:
    name: str
    blocks: list[MachineBlock]

@dataclass
class MachineProgram:
    functions: list[MachineFunction]
