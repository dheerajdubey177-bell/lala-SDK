from .machine_ir import MachineFunction, MachineInstruction, MachineOperand, Immediate, MemoryOperand, LabelOperand
from .registers import X86Register
from .instruction_forms import ALLOWED_FORMS

class MachineValidationError(Exception):
    pass

class MachineValidator:
    def validate(self, mfunc: MachineFunction):
        # Gather all valid labels
        valid_labels = {block.name for block in mfunc.blocks}
        
        for block in mfunc.blocks:
            for instr in block.instructions:
                self._validate_instruction(instr, valid_labels)
                
    def _validate_instruction(self, instr: MachineInstruction, valid_labels: set[str]):
        # Check opcode form
        if instr.opcode not in ALLOWED_FORMS:
            raise MachineValidationError(f"Unknown opcode: {instr.opcode}")
            
        forms = ALLOWED_FORMS[instr.opcode]
        
        # Check if current operands match any allowed form
        op_types = tuple(type(op) for op in instr.operands)
        
        # We need to map types to R, I, M, L
        def map_type(t):
            if issubclass(t, X86Register): return X86Register
            if issubclass(t, Immediate): return Immediate
            if issubclass(t, MemoryOperand): return MemoryOperand
            if issubclass(t, LabelOperand): return LabelOperand
            return t
            
        mapped_types = tuple(map_type(t) for t in op_types)
        
        if mapped_types not in forms:
            raise MachineValidationError(f"Invalid operands for {instr.opcode}: {mapped_types}. Allowed: {forms}")
            
        # Check specific constraints
        # 1. No memory-to-memory
        mem_count = sum(1 for op in instr.operands if isinstance(op, MemoryOperand))
        if mem_count > 1:
            raise MachineValidationError(f"Memory-to-memory operation not allowed: {instr}")
            
        # 2. Check valid labels
        for op in instr.operands:
            if isinstance(op, LabelOperand):
                # Basic check, though external calls might not be in valid_labels
                # We assume external calls don't start with .L
                if op.name.startswith(".L") and op.name not in valid_labels:
                    raise MachineValidationError(f"Branch to unknown label: {op.name}")
