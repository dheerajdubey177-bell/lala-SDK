from compiler.mir.core import MachineType
from .target import TargetBackend
from .register_file import RegisterFile, PhysicalRegister, RegisterClass
from .calling_convention import CallingConvention, PassedInRegister, ReturnedInRegister
from .instruction_set import InstructionSet
from .stack_model import StackModel
from .data_layout import DataLayout

# A minimal Register File with 8 GPRs for testing
_REGS = [
    PhysicalRegister(id=i, name=f"P{i}", reg_class=RegisterClass.GENERAL_PURPOSE, width=8, caller_saved=(i<4), callee_saved=(i>=4))
    for i in range(8)
]

class ReferenceCallingConvention(CallingConvention):
    def how_is_passed(self, type_obj: MachineType, arg_index: int):
        # Pass first 4 args in P0-P3
        if arg_index < 4:
            return PassedInRegister(_REGS[arg_index])
        raise NotImplementedError("Stack passing not implemented for reference target")
        
    def how_is_returned(self, type_obj: MachineType):
        return ReturnedInRegister(_REGS[0])
        
    def get_preserved_registers(self) -> list[PhysicalRegister]:
        return [r for r in _REGS if r.callee_saved]
        
    def get_scratch_registers(self) -> list[PhysicalRegister]:
        return [r for r in _REGS if r.caller_saved]
        
    def stack_alignment_at_call(self) -> int:
        return 16

class ReferenceTarget(TargetBackend):
    @property
    def name(self) -> str: return "ref-unknown-unknown"
    @property
    def architecture(self) -> str: return "ref"
    @property
    def operating_system(self) -> str: return "unknown"
    @property
    def abi_name(self) -> str: return "unknown"
    @property
    def pointer_size(self) -> int: return 8
    @property
    def endianness(self) -> str: return "little"

    def register_file(self) -> RegisterFile:
        return RegisterFile(_REGS)

    def calling_convention(self) -> CallingConvention:
        return ReferenceCallingConvention()

    def instruction_set(self) -> InstructionSet:
        return InstructionSet() # Defaults are basic arithmetic

    def stack_model(self) -> StackModel:
        return StackModel()

    def data_layout(self) -> DataLayout:
        return DataLayout(endianness="little", pointer_size=8)
