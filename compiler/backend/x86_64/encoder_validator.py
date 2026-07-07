from .machine_ir import MachineInstruction, MachineOperand, Immediate, MemoryOperand, LabelOperand
from .registers import X86Register
from .opcodes import Opcode

class EncoderValidator:
    def validate(self, instr: MachineInstruction):
        # Validate that the instruction opcode is supported
        pass
