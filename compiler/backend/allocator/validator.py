from compiler.mir.core import (
    Function, Terminator, VirtualRegister, StackSlot, Instruction
)
from compiler.backend.register_file import PhysicalRegister
from compiler.backend.target import TargetBackend

class PMIRValidationError(Exception):
    pass

class PMIRValidator:
    def __init__(self, target: TargetBackend):
        self.target = target
        self.valid_phys_regs = {r.id for r in target.register_file().get_all()}
        
    def validate(self, pmir_func: Function):
        # We will collect all operands to ensure no VirtualRegisters slipped through
        for block in pmir_func.blocks:
            if not block.instructions:
                continue
                
            # 1. Exactly one terminator, and it must be the last instruction
            term_count = sum(1 for i in block.instructions if isinstance(i, Terminator))
            if term_count != 1:
                raise PMIRValidationError(f"Block {block.id} must have exactly one terminator, found {term_count}")
                
            if not isinstance(block.instructions[-1], Terminator):
                raise PMIRValidationError(f"Block {block.id} terminator must be the last instruction")
                
            # 2. Check all operands are PhysicalRegister or StackSlot, NEVER VirtualRegister
            for instr in block.instructions:
                self._validate_operands(instr)

    def _validate_operands(self, instr: Instruction):
        # We reflectively extract all attributes
        for key, value in vars(instr).items():
            if isinstance(value, VirtualRegister):
                raise PMIRValidationError(f"VirtualRegister {value} leaked into PMIR! Instruction: {instr}")
                
            if isinstance(value, PhysicalRegister):
                if value.id not in self.valid_phys_regs:
                    raise PMIRValidationError(f"Invalid physical register {value.name} used in PMIR")
