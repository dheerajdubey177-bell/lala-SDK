from .core import *
from .builder import MIRBuilder

class MIROptimizationPass:
    def optimize(self, program: Program) -> tuple[Program, bool]:
        raise NotImplementedError()

class CopyPropagationPass(MIROptimizationPass):
    def optimize(self, program: Program) -> tuple[Program, bool]:
        changed = False
        new_prog = Program()
        
        for func in program.functions:
            new_func = Function(func.name)
            new_prog.functions.append(new_func)
            
            # Map vreg -> vreg (source of truth)
            copy_map = {}
            
            for block in func.blocks:
                new_block = BasicBlock(block.id)
                new_func.add_block(new_block)
                
                for instr in block.instructions:
                    # Resolve sources through copy_map
                    if hasattr(instr, "source") and isinstance(instr.source, VirtualRegister):
                        if instr.source.id in copy_map:
                            instr.source = copy_map[instr.source.id]
                            changed = True
                    if hasattr(instr, "left") and isinstance(instr.left, VirtualRegister):
                        if instr.left.id in copy_map:
                            instr.left = copy_map[instr.left.id]
                            changed = True
                    if hasattr(instr, "right") and isinstance(instr.right, VirtualRegister):
                        if instr.right.id in copy_map:
                            instr.right = copy_map[instr.right.id]
                            changed = True
                    if hasattr(instr, "operand") and isinstance(instr.operand, VirtualRegister):
                        if instr.operand.id in copy_map:
                            instr.operand = copy_map[instr.operand.id]
                            changed = True
                    if hasattr(instr, "condition") and isinstance(instr.condition, VirtualRegister):
                        if instr.condition.id in copy_map:
                            instr.condition = copy_map[instr.condition.id]
                            changed = True
                    if hasattr(instr, "value") and isinstance(instr.value, VirtualRegister):
                        if instr.value.id in copy_map:
                            instr.value = copy_map[instr.value.id]
                            changed = True
                    
                    if isinstance(instr, MoveInstruction):
                        # Register the copy
                        copy_map[instr.target.id] = instr.source
                        
                    new_block.add(instr)
                    
        return new_prog, changed

class DeadMoveEliminationPass(MIROptimizationPass):
    def optimize(self, program: Program) -> tuple[Program, bool]:
        changed = False
        new_prog = Program()
        
        for func in program.functions:
            new_func = Function(func.name)
            new_prog.functions.append(new_func)
            
            # 1. Find all used registers
            used = set()
            for block in func.blocks:
                for instr in block.instructions:
                    if hasattr(instr, "source") and isinstance(instr.source, VirtualRegister):
                        used.add(instr.source.id)
                    if hasattr(instr, "left") and isinstance(instr.left, VirtualRegister):
                        used.add(instr.left.id)
                    if hasattr(instr, "right") and isinstance(instr.right, VirtualRegister):
                        used.add(instr.right.id)
                    if hasattr(instr, "operand") and isinstance(instr.operand, VirtualRegister):
                        used.add(instr.operand.id)
                    if hasattr(instr, "condition") and isinstance(instr.condition, VirtualRegister):
                        used.add(instr.condition.id)
                    if hasattr(instr, "value") and isinstance(instr.value, VirtualRegister):
                        used.add(instr.value.id)
                        
            # 2. Filter out moves to unused registers
            for block in func.blocks:
                new_block = BasicBlock(block.id)
                new_func.add_block(new_block)
                for instr in block.instructions:
                    if isinstance(instr, MoveInstruction) and instr.target.id not in used:
                        changed = True
                        continue
                    new_block.add(instr)
                    
        return new_prog, changed

class PeepholeOptimizationPass(MIROptimizationPass):
    def optimize(self, program: Program) -> tuple[Program, bool]:
        changed = False
        new_prog = Program()
        
        # Simple tracking of constants within a block
        for func in program.functions:
            new_func = Function(func.name)
            new_prog.functions.append(new_func)
            
            for block in func.blocks:
                new_block = BasicBlock(block.id)
                new_func.add_block(new_block)
                
                const_map = {}
                
                for instr in block.instructions:
                    if isinstance(instr, ConstInstruction):
                        const_map[instr.target.id] = instr.value
                        new_block.add(instr)
                        continue
                        
                    if isinstance(instr, BinaryInstruction):
                        op = instr.op
                        l_id = instr.left.id
                        r_id = instr.right.id
                        
                        l_val = const_map.get(l_id)
                        r_val = const_map.get(r_id)
                        
                        # add x, 0 -> mov x
                        if op == "add" and r_val == 0:
                            new_block.add(MoveInstruction(instr.target, instr.left))
                            changed = True
                            continue
                        elif op == "add" and l_val == 0:
                            new_block.add(MoveInstruction(instr.target, instr.right))
                            changed = True
                            continue
                        
                        # mul x, 1 -> mov x
                        if op == "mul" and r_val == 1:
                            new_block.add(MoveInstruction(instr.target, instr.left))
                            changed = True
                            continue
                        elif op == "mul" and l_val == 1:
                            new_block.add(MoveInstruction(instr.target, instr.right))
                            changed = True
                            continue
                    
                    # mov x, x -> eliminate? That's useful too, but let's stick to the ones requested.
                    new_block.add(instr)
                    
        return new_prog, changed

class StackSlotSimplificationPass(MIROptimizationPass):
    def optimize(self, program: Program) -> tuple[Program, bool]:
        changed = False
        new_prog = Program()
        
        for func in program.functions:
            new_func = Function(func.name)
            new_prog.functions.append(new_func)
            
            for block in func.blocks:
                new_block = BasicBlock(block.id)
                new_func.add_block(new_block)
                
                # stack_id -> virtual_register recently stored there
                stack_state = {}
                
                for instr in block.instructions:
                    if isinstance(instr, StoreInstruction) and isinstance(instr.target_ptr, StackSlot):
                        stack_state[instr.target_ptr.id] = instr.source
                        new_block.add(instr)
                    elif isinstance(instr, LoadInstruction) and isinstance(instr.source_ptr, StackSlot):
                        # If we just stored this value, bypass the stack!
                        slot_id = instr.source_ptr.id
                        if slot_id in stack_state:
                            source = stack_state[slot_id]
                            new_block.add(MoveInstruction(instr.target, source))
                            changed = True
                            continue
                        else:
                            new_block.add(instr)
                    else:
                        new_block.add(instr)
                        
        return new_prog, changed

class CFGCleanupPass(MIROptimizationPass):
    def optimize(self, program: Program) -> tuple[Program, bool]:
        changed = False
        new_prog = Program()
        
        for func in program.functions:
            new_func = Function(func.name)
            new_prog.functions.append(new_func)
            
            # Determine reachability
            reachable = set()
            if func.blocks:
                reachable.add(func.blocks[0].id.id)
                queue = [func.blocks[0]]
                while queue:
                    curr = queue.pop(0)
                    term = curr.terminator
                    if isinstance(term, JumpInstruction):
                        if term.target_block.id not in reachable:
                            reachable.add(term.target_block.id)
                            target = next(b for b in func.blocks if b.id.id == term.target_block.id)
                            queue.append(target)
                    elif isinstance(term, BranchInstruction):
                        for target_id in (term.true_block.id, term.false_block.id):
                            if target_id not in reachable:
                                reachable.add(target_id)
                                target = next(b for b in func.blocks if b.id.id == target_id)
                                queue.append(target)
            
            block_map = {b.id.id: b for b in func.blocks}
            
            for block in func.blocks:
                if block.id.id not in reachable:
                    changed = True
                    continue # unreachable
                    
                new_block = BasicBlock(block.id)
                new_func.add_block(new_block)
                
                for instr in block.instructions:
                    if isinstance(instr, JumpInstruction):
                        target_b = block_map.get(instr.target_block.id)
                        if target_b and len(target_b.instructions) == 1 and isinstance(target_b.instructions[0], JumpInstruction):
                            next_target = target_b.instructions[0].target_block
                            if next_target.id != block.id.id:
                                new_block.add(JumpInstruction(next_target))
                                changed = True
                                continue
                    new_block.add(instr)
                    
        return new_prog, changed

class MIROptimizationPipeline:
    def __init__(self):
        self.passes = [
            CopyPropagationPass(),
            DeadMoveEliminationPass(),
            PeepholeOptimizationPass(),
            StackSlotSimplificationPass(),
            CFGCleanupPass()
        ]
        
    def run(self, program: Program) -> Program:
        max_iters = 5
        curr_prog = program
        
        for _ in range(max_iters):
            pipeline_changed = False
            for p in self.passes:
                curr_prog, changed = p.optimize(curr_prog)
                if changed:
                    pipeline_changed = True
                    
            if not pipeline_changed:
                break
                
        return curr_prog
