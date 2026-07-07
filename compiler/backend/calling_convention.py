from dataclasses import dataclass
from typing import Union
from compiler.mir.core import MachineType
from .register_file import PhysicalRegister

@dataclass(frozen=True)
class PassedInRegister:
    register: PhysicalRegister

@dataclass(frozen=True)
class PassedOnStack:
    alignment: int
    size: int

PassLocation = Union[PassedInRegister, PassedOnStack]

@dataclass(frozen=True)
class ReturnedInRegister:
    register: PhysicalRegister

@dataclass(frozen=True)
class ReturnedViaHiddenPointer:
    pass

ReturnLocation = Union[ReturnedInRegister, ReturnedViaHiddenPointer]

class CallingConvention:
    def how_is_passed(self, type_obj: MachineType, arg_index: int) -> PassLocation:
        raise NotImplementedError()
        
    def how_is_returned(self, type_obj: MachineType) -> ReturnLocation:
        raise NotImplementedError()
        
    def get_preserved_registers(self) -> list[PhysicalRegister]:
        """Registers the callee must save and restore if used."""
        raise NotImplementedError()
        
    def get_scratch_registers(self) -> list[PhysicalRegister]:
        """Registers the caller must assume are clobbered."""
        raise NotImplementedError()
        
    def stack_alignment_at_call(self) -> int:
        """Required stack alignment before executing the call instruction (e.g., 16 for x86-64)."""
        raise NotImplementedError()
