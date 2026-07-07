from .core import *

class HIRValidationError(Exception):
    pass

class HIRValidator:
    def validate(self, program: Program):
        for func in program.functions:
            self._validate_function(func)

    def _validate_function(self, func: Function):
        block_ids = {b.id.id for b in func.blocks}
        defined_values = set()
        
        for block in func.blocks:
            if not block.instructions:
                raise HIRValidationError(f"Block {block.id} in {func.name} is empty.")
                
            # Rule 1: Every block ends in exactly one terminator
            if not isinstance(block.instructions[-1], Terminator):
                raise HIRValidationError(f"Block {block.id} in {func.name} does not end with a Terminator.")
                
            for i, instr in enumerate(block.instructions):
                # Ensure no terminators in the middle of a block
                if isinstance(instr, Terminator) and i != len(block.instructions) - 1:
                    raise HIRValidationError(f"Block {block.id} in {func.name} has a terminator before the end.")
                    
                # Rule 2: Every ValueID is defined before use.
                # (Simple linear check within the block for now, SSA will require dominator trees later)
                # For v1, we just track defined values globally in the function. 
                # Since we generate strictly linear assignments in the builder, a simple set works for now.
                if instr.target:
                    defined_values.add(instr.target.id)
                    
                self._validate_instruction_usage(instr, defined_values, block_ids, func.name)

    def _validate_instruction_usage(self, instr: Instruction, defined_values: set, block_ids: set, func_name: str):
        def check_val(val: ValueID):
            if val.id not in defined_values:
                raise HIRValidationError(f"Value {val} used before definition in {func_name}.")

        if isinstance(instr, Load):
            check_val(instr.source_ptr)
        elif isinstance(instr, Store):
            check_val(instr.target_ptr)
            check_val(instr.value)
        elif isinstance(instr, BinaryOp):
            check_val(instr.left)
            check_val(instr.right)
        elif isinstance(instr, UnaryOp):
            check_val(instr.operand)
        elif isinstance(instr, IntrinsicCall):
            for arg in instr.args:
                check_val(arg)
        elif isinstance(instr, RuntimeCall):
            for arg in instr.args:
                check_val(arg)
        elif isinstance(instr, Branch):
            check_val(instr.condition)
            if instr.true_block.id not in block_ids:
                raise HIRValidationError(f"Branch target {instr.true_block} does not exist in {func_name}.")
            if instr.false_block.id not in block_ids:
                raise HIRValidationError(f"Branch target {instr.false_block} does not exist in {func_name}.")
        elif isinstance(instr, Jump):
            if instr.target_block.id not in block_ids:
                raise HIRValidationError(f"Jump target {instr.target_block} does not exist in {func_name}.")
        elif isinstance(instr, Return):
            if instr.value:
                check_val(instr.value)
