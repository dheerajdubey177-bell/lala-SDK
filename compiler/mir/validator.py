from .core import *

class MIRValidationError(Exception):
    pass

class MIRValidator:
    def validate(self, program: Program):
        for func in program.functions:
            self._validate_function(func)

    def _validate_function(self, func: Function):
        block_ids = {b.id.id for b in func.blocks}
        defined_vregs = {} # id -> MachineType
        
        # Pass 1: Ensure every virtual register is defined exactly once, 
        # and ensure basic block structure is correct.
        for block in func.blocks:
            if not block.instructions:
                raise MIRValidationError(f"Block {block.id} in {func.name} is empty.")
                
            has_terminator = False
            for i, instr in enumerate(block.instructions):
                if isinstance(instr, Terminator):
                    if i != len(block.instructions) - 1:
                        raise MIRValidationError(f"Block {block.id} in {func.name} has instructions after terminator.")
                    has_terminator = True
                    
                target = getattr(instr, "target", None)
                if isinstance(target, VirtualRegister):
                    if target.id in defined_vregs:
                        raise MIRValidationError(f"VirtualRegister v{target.id} defined multiple times in {func.name}.")
                    defined_vregs[target.id] = target.type
                    
            if not has_terminator:
                raise MIRValidationError(f"Block {block.id} in {func.name} missing terminator.")
                
        # Pass 2: Check uses, types, and invariants
        for block in func.blocks:
            next_arg_index = 0
            for instr in block.instructions:
                self._validate_instruction(instr, defined_vregs, block_ids, func.name)
                
                # Check call arg contiguousness
                if isinstance(instr, SetArgInstruction):
                    if instr.index != next_arg_index:
                        raise MIRValidationError(f"SetArg index {instr.index} out of order in {func.name}. Expected {next_arg_index}.")
                    next_arg_index += 1
                elif isinstance(instr, CallInstruction):
                    next_arg_index = 0 # Reset after call
                    
    def _validate_instruction(self, instr: Instruction, defined_vregs: dict[int, MachineType], block_ids: set[int], func_name: str):
        def check_use(reg: VirtualRegister):
            if reg.id not in defined_vregs:
                raise MIRValidationError(f"VirtualRegister v{reg.id} used before definition in {func_name}.")
            if reg.type != defined_vregs[reg.id]:
                raise MIRValidationError(f"VirtualRegister v{reg.id} type mismatch: {reg.type} vs {defined_vregs[reg.id]}")
                
        def check_ptr(reg_or_slot):
            if isinstance(reg_or_slot, VirtualRegister):
                check_use(reg_or_slot)
                if reg_or_slot.type != MachineType.PTR:
                    raise MIRValidationError(f"Expected PTR, got {reg_or_slot.type} in {func_name}.")
            elif not isinstance(reg_or_slot, StackSlot):
                raise MIRValidationError(f"Expected PTR or StackSlot, got {type(reg_or_slot)} in {func_name}.")

        if isinstance(instr, ConstInstruction):
            pass
        elif isinstance(instr, MoveInstruction):
            check_use(instr.source)
            if instr.target.type != instr.source.type:
                raise MIRValidationError(f"Move type mismatch: {instr.target.type} != {instr.source.type} in {func_name}.")
        elif isinstance(instr, BinaryInstruction):
            check_use(instr.left)
            check_use(instr.right)
            if instr.left.type != instr.right.type or instr.left.type != instr.target.type:
                raise MIRValidationError(f"Binary op type mismatch in {func_name}.")
        elif isinstance(instr, UnaryInstruction):
            check_use(instr.operand)
            if instr.operand.type != instr.target.type:
                raise MIRValidationError(f"Unary op type mismatch in {func_name}.")
        elif isinstance(instr, CompareInstruction):
            check_use(instr.left)
            check_use(instr.right)
            if instr.target.type != MachineType.I1:
                raise MIRValidationError(f"Compare target must be i1 in {func_name}.")
            if instr.left.type != instr.right.type:
                raise MIRValidationError(f"Compare operand type mismatch in {func_name}.")
        elif isinstance(instr, LoadInstruction):
            check_ptr(instr.source_ptr)
        elif isinstance(instr, StoreInstruction):
            check_ptr(instr.target_ptr)
            check_use(instr.source)
        elif isinstance(instr, SetArgInstruction):
            check_use(instr.value)
        elif isinstance(instr, JumpInstruction):
            if instr.target_block.id not in block_ids:
                raise MIRValidationError(f"Jump target b{instr.target_block.id} does not exist in {func_name}.")
        elif isinstance(instr, BranchInstruction):
            check_use(instr.condition)
            if instr.condition.type != MachineType.I1:
                raise MIRValidationError(f"Branch condition must be i1 in {func_name}.")
            if instr.true_block.id not in block_ids or instr.false_block.id not in block_ids:
                raise MIRValidationError(f"Branch target does not exist in {func_name}.")
        elif isinstance(instr, ReturnInstruction):
            if instr.value:
                check_use(instr.value)
