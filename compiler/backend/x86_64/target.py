from compiler.backend.target import TargetBackend
from compiler.backend.register_file import RegisterFile, PhysicalRegister
from compiler.backend.calling_convention import CallingConvention, PassedInRegister, ReturnedInRegister
from compiler.backend.instruction_set import InstructionSet
from compiler.backend.stack_model import StackModel
from compiler.backend.data_layout import DataLayout
from compiler.mir.core import MachineType

from .registers import ALL_GPRS, RAX, RDI, RSI, RDX, RCX, R8, R9

# System V AMD64 ABI Caller/Callee saved regs
# (Simplified: ignoring XMMs and others for now)
_CALLER_SAVED = [RAX, RCX, RDX, RSI, RDI, R8, R9, ALL_GPRS[10], ALL_GPRS[11]] # R10, R11
_CALLEE_SAVED = [ALL_GPRS[1], ALL_GPRS[6], ALL_GPRS[12], ALL_GPRS[13], ALL_GPRS[14], ALL_GPRS[15]] # RBX, RBP, R12-R15

class SystemVCallingConvention(CallingConvention):
    def how_is_passed(self, type_obj: MachineType, arg_index: int):
        regs = [RDI, RSI, RDX, RCX, R8, R9]
        if arg_index < len(regs):
            # We map our custom X86Register to the backend PhysicalRegister type based on ID
            return PassedInRegister(PhysicalRegister(regs[arg_index].id, regs[arg_index].name, None, 64))
        raise NotImplementedError("Stack passing not implemented for x86-64 System V")
        
    def how_is_returned(self, type_obj: MachineType):
        return ReturnedInRegister(PhysicalRegister(RAX.id, RAX.name, None, 64))
        
    def get_preserved_registers(self) -> list[PhysicalRegister]:
        return [PhysicalRegister(r.id, r.name, None, 64) for r in _CALLEE_SAVED]
        
    def get_scratch_registers(self) -> list[PhysicalRegister]:
        return [PhysicalRegister(r.id, r.name, None, 64) for r in _CALLER_SAVED]
        
    def stack_alignment_at_call(self) -> int:
        return 16

class X86_64Target(TargetBackend):
    @property
    def name(self) -> str: return "x86_64-unknown-linux-gnu"
    @property
    def architecture(self) -> str: return "x86_64"
    @property
    def operating_system(self) -> str: return "linux"
    @property
    def abi_name(self) -> str: return "sysv"
    @property
    def pointer_size(self) -> int: return 8
    @property
    def endianness(self) -> str: return "little"

    def register_file(self) -> RegisterFile:
        from compiler.backend.register_file import RegisterClass
        phys = []
        for r in ALL_GPRS:
            caller = r in _CALLER_SAVED
            callee = r in _CALLEE_SAVED
            phys.append(PhysicalRegister(r.id, r.name, RegisterClass.GENERAL_PURPOSE, 64, caller, callee))
        return RegisterFile(phys)

    def calling_convention(self) -> CallingConvention:
        return SystemVCallingConvention()

    def instruction_set(self) -> InstructionSet:
        return InstructionSet() 

    def stack_model(self) -> StackModel:
        return StackModel()

    def data_layout(self) -> DataLayout:
        return DataLayout(endianness="little", pointer_size=8)
