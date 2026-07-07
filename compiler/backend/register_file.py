from enum import Enum, auto
from dataclasses import dataclass

class RegisterClass(Enum):
    GENERAL_PURPOSE = auto()
    FLOATING_POINT = auto()
    VECTOR = auto()
    PREDICATE = auto()
    SPECIAL = auto()

@dataclass(frozen=True)
class PhysicalRegister:
    id: int
    name: str
    reg_class: RegisterClass
    width: int # in bytes
    allocatable: bool = True
    caller_saved: bool = False
    callee_saved: bool = False

class RegisterFile:
    def __init__(self, registers: list[PhysicalRegister]):
        self.registers = registers
        self._by_class = {}
        for r in registers:
            self._by_class.setdefault(r.reg_class, []).append(r)
            
    def get_all(self) -> list[PhysicalRegister]:
        return self.registers
        
    def get_class(self, reg_class: RegisterClass) -> list[PhysicalRegister]:
        return self._by_class.get(reg_class, [])
        
    def allocatable(self, reg_class: RegisterClass) -> list[PhysicalRegister]:
        return [r for r in self.get_class(reg_class) if r.allocatable]
