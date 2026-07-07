from compiler.mir.core import (
    Function, BasicBlock, BlockID, VirtualRegister, StackSlot,
    LoadInstruction, StoreInstruction
)
from compiler.backend.allocator.linear_scan import AllocationContext

class SpillInsertionPass:
    def __init__(self, ctx: AllocationContext):
        self.ctx = ctx
        self.next_temp_id = 10000 # High enough to not collide with normal vregs
        
        # Get scratch registers from calling convention
        # We assume we have at least one scratch register for memory ops
        self.scratch_regs = ctx.target.calling_convention().get_scratch_registers()
        if not self.scratch_regs:
            # Fallback to general purpose if no explicit scratch
            from compiler.backend.register_file import RegisterClass
            self.scratch_regs = ctx.target.register_file().allocatable(RegisterClass.GENERAL_PURPOSE)
            
    def run(self, func: Function) -> Function:
        new_func = Function(func.name)
        
        for block in func.blocks:
            new_block = BasicBlock(BlockID(block.id.id))
            
            for instr in block.instructions:
                # Find defs and uses
                from compiler.backend.allocator.liveness import _get_def_use
                defs, uses = _get_def_use(instr)
                
                # Check for spilled uses
                spilled_uses = {u for u in uses if u.id in self.ctx.spill_mapping}
                use_replacements = {}
                
                scratch_idx = 0
                for u in spilled_uses:
                    # Allocate a temp virtual register
                    v_temp = VirtualRegister(self.next_temp_id, u.type)
                    self.next_temp_id += 1
                    
                    # Map this temp vreg to a physical scratch register
                    scratch_phys = self.scratch_regs[scratch_idx % len(self.scratch_regs)]
                    self.ctx.register_mapping[v_temp.id] = scratch_phys
                    scratch_idx += 1
                    
                    # Insert Load: v_temp = load spillX
                    spill_slot = StackSlot(self.ctx.spill_mapping[u.id])
                    new_block.add(LoadInstruction(v_temp, spill_slot))
                    
                    use_replacements[u] = v_temp
                    
                # Replace uses in instruction
                # We do this by creating a new instruction or simply mutating the generic parameters.
                # Since we want MIR->MIR immutability, we should conceptually create a new instruction.
                # For simplicity here, we'll recreate the instruction with replacements.
                new_instr = self._recreate_instruction_with_replacements(instr, use_replacements, {})
                
                # Check for spilled defs
                spilled_defs = {d for d in defs if d.id in self.ctx.spill_mapping}
                def_replacements = {}
                
                for d in spilled_defs:
                    v_temp = VirtualRegister(self.next_temp_id, d.type)
                    self.next_temp_id += 1
                    
                    scratch_phys = self.scratch_regs[scratch_idx % len(self.scratch_regs)]
                    self.ctx.register_mapping[v_temp.id] = scratch_phys
                    scratch_idx += 1
                    
                    def_replacements[d] = v_temp
                    
                if def_replacements:
                    new_instr = self._recreate_instruction_with_replacements(new_instr, {}, def_replacements)
                    
                new_block.add(new_instr)
                
                # Insert Store for defs: store spillX, v_temp
                for d, v_temp in def_replacements.items():
                    spill_slot = StackSlot(self.ctx.spill_mapping[d.id])
                    new_block.add(StoreInstruction(spill_slot, v_temp))
                    
            new_func.add_block(new_block)
            
        return new_func

    def _recreate_instruction_with_replacements(self, instr, use_replacements, def_replacements):
        from compiler.mir.core import (
            ConstInstruction, MoveInstruction, BinaryInstruction, UnaryInstruction,
            CompareInstruction, LoadInstruction, StoreInstruction,
            SetArgInstruction, CallInstruction, GetRetvalInstruction,
            BranchInstruction, ReturnInstruction, JumpInstruction
        )
        
        def rep(v):
            return use_replacements.get(v, def_replacements.get(v, v))
            
        if isinstance(instr, ConstInstruction):
            return ConstInstruction(rep(instr.target), instr.value)
        elif isinstance(instr, MoveInstruction):
            return MoveInstruction(rep(instr.target), rep(instr.source))
        elif isinstance(instr, BinaryInstruction):
            return BinaryInstruction(rep(instr.target), instr.op, rep(instr.left), rep(instr.right))
        elif isinstance(instr, UnaryInstruction):
            return UnaryInstruction(rep(instr.target), instr.op, rep(instr.operand))
        elif isinstance(instr, CompareInstruction):
            return CompareInstruction(rep(instr.target), instr.op, rep(instr.left), rep(instr.right))
        elif isinstance(instr, LoadInstruction):
            return LoadInstruction(rep(instr.target), rep(instr.source_ptr))
        elif isinstance(instr, StoreInstruction):
            return StoreInstruction(rep(instr.target_ptr), rep(instr.source))
        elif isinstance(instr, SetArgInstruction):
            return SetArgInstruction(instr.index, rep(instr.value))
        elif isinstance(instr, CallInstruction):
            return CallInstruction(instr.func_name)
        elif isinstance(instr, GetRetvalInstruction):
            return GetRetvalInstruction(rep(instr.target))
        elif isinstance(instr, BranchInstruction):
            return BranchInstruction(rep(instr.condition), instr.true_block, instr.false_block)
        elif isinstance(instr, ReturnInstruction):
            return ReturnInstruction(rep(instr.value) if instr.value else None)
        elif isinstance(instr, JumpInstruction):
            return JumpInstruction(instr.target_block)
            
        return instr
