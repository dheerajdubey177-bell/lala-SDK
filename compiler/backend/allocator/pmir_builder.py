from compiler.mir.core import (
    Function, BasicBlock, BlockID, VirtualRegister, StackSlot,
    ConstInstruction, MoveInstruction, BinaryInstruction, UnaryInstruction,
    CompareInstruction, LoadInstruction, StoreInstruction,
    SetArgInstruction, CallInstruction, GetRetvalInstruction,
    BranchInstruction, ReturnInstruction, JumpInstruction
)
from compiler.backend.register_file import PhysicalRegister
from compiler.backend.allocator.linear_scan import AllocationContext

class PMIRBuilder:
    def __init__(self, ctx: AllocationContext):
        self.ctx = ctx
        
    def build(self, func: Function) -> Function:
        """Immutable transformation from MIR to PMIR."""
        pmir_func = Function(func.name)
        
        for block in func.blocks:
            pmir_block = BasicBlock(BlockID(block.id.id))
            
            for instr in block.instructions:
                pmir_instr = self._translate_instruction(instr)
                pmir_block.add(pmir_instr)
                
            pmir_func.add_block(pmir_block)
            
        return pmir_func
        
    def _translate_register(self, vreg: VirtualRegister) -> PhysicalRegister:
        if vreg.id in self.ctx.register_mapping:
            return self.ctx.register_mapping[vreg.id]
        raise RuntimeError(f"Virtual register {vreg} was not allocated a physical register.")
        
    def _translate_memory(self, mem: StackSlot) -> StackSlot:
        # Currently identity, but could be transformed to explicit frame offsets later
        return mem
        
    def _translate_op(self, op: VirtualRegister | StackSlot) -> PhysicalRegister | StackSlot:
        if isinstance(op, VirtualRegister):
            return self._translate_register(op)
        elif isinstance(op, StackSlot):
            return self._translate_memory(op)
        return op

    def _translate_instruction(self, instr):
        # We structurally recreate every instruction to ensure immutability
        if isinstance(instr, ConstInstruction):
            return ConstInstruction(self._translate_register(instr.target), instr.value)
            
        elif isinstance(instr, MoveInstruction):
            return MoveInstruction(
                self._translate_register(instr.target),
                self._translate_register(instr.source)
            )
            
        elif isinstance(instr, BinaryInstruction):
            return BinaryInstruction(
                self._translate_register(instr.target),
                instr.op,
                self._translate_register(instr.left),
                self._translate_register(instr.right)
            )
            
        elif isinstance(instr, UnaryInstruction):
            return UnaryInstruction(
                self._translate_register(instr.target),
                instr.op,
                self._translate_register(instr.operand)
            )
            
        elif isinstance(instr, CompareInstruction):
            return CompareInstruction(
                self._translate_register(instr.target),
                instr.op,
                self._translate_register(instr.left),
                self._translate_register(instr.right)
            )
            
        elif isinstance(instr, LoadInstruction):
            return LoadInstruction(
                self._translate_register(instr.target),
                self._translate_op(instr.source_ptr)
            )
            
        elif isinstance(instr, StoreInstruction):
            return StoreInstruction(
                self._translate_op(instr.target_ptr),
                self._translate_register(instr.source)
            )
            
        elif isinstance(instr, SetArgInstruction):
            return SetArgInstruction(
                instr.index,
                self._translate_register(instr.value)
            )
            
        elif isinstance(instr, CallInstruction):
            return CallInstruction(instr.func_name)
            
        elif isinstance(instr, GetRetvalInstruction):
            return GetRetvalInstruction(self._translate_register(instr.target))
            
        elif isinstance(instr, BranchInstruction):
            return BranchInstruction(
                self._translate_register(instr.condition),
                instr.true_block,
                instr.false_block
            )
            
        elif isinstance(instr, ReturnInstruction):
            return ReturnInstruction(
                self._translate_register(instr.value) if instr.value else None
            )
            
        elif isinstance(instr, JumpInstruction):
            return JumpInstruction(instr.target_block)
            
        raise NotImplementedError(f"Unsupported instruction type in PMIR Builder: {type(instr)}")
