from compiler.hir.core import *
from compiler.context import CompilationContext
from .pass_manager import OptimizationPass, OptimizationResult
from .ir_builder import IRBuilder
from .constant_evaluator import ConstantEvaluator

class ConstantFoldingPass(OptimizationPass):
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        builder = IRBuilder(program)
        evaluator = ConstantEvaluator(context)
        
        constants = {} # ValueID.id -> value
        stats = {"folded": 0}
        
        for func in program.functions:
            builder.start_function(func.name)
            
            for block in func.blocks:
                block_changed = False
                new_instructions = []
                
                for instr in block.instructions:
                    # Collect constants
                    if isinstance(instr, Constant):
                        constants[instr.target.id] = instr.value
                        new_instructions.append(instr)
                        continue
                        
                    # Attempt to fold binary ops
                    if isinstance(instr, BinaryOp):
                        if instr.left.id in constants and instr.right.id in constants:
                            left_val = constants[instr.left.id]
                            right_val = constants[instr.right.id]
                            
                            folded_val = evaluator.evaluate_binary(instr.op, left_val, right_val, instr.type)
                            if folded_val is not None:
                                constants[instr.target.id] = folded_val
                                new_instructions.append(Constant(instr.target, instr.type, folded_val))
                                block_changed = True
                                builder.mark_changed()
                                stats["folded"] += 1
                                continue
                                
                    # If not folded, keep instruction
                    new_instructions.append(instr)
                    
                if block_changed:
                    builder.start_block(block.id)
                    for instr in new_instructions:
                        builder.add_instruction(instr)
                else:
                    builder.reuse_block(block)
                    
        return OptimizationResult(builder.new_program, builder.changed, stats)

class ConstantPropagationPass(OptimizationPass):
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        return OptimizationResult(program, False, {})

class ConstantBranchFoldingPass(OptimizationPass):
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        builder = IRBuilder(program)
        stats = {"branches_folded": 0}
        
        for func in program.functions:
            builder.start_function(func.name)
            
            for block in func.blocks:
                block_changed = False
                new_instructions = []
                
                # We need to know if the terminator's condition is a constant.
                # To do this safely within a block, we track constants locally.
                local_constants = {}
                
                for instr in block.instructions:
                    if isinstance(instr, Constant):
                        local_constants[instr.target.id] = instr.value
                        new_instructions.append(instr)
                    elif isinstance(instr, Branch) and instr.condition.id in local_constants:
                        cond_val = local_constants[instr.condition.id]
                        
                        target_block_id = instr.true_block if cond_val else instr.false_block
                        new_instructions.append(Jump(target_block_id))
                        
                        block_changed = True
                        builder.mark_changed()
                        stats["branches_folded"] += 1
                    else:
                        new_instructions.append(instr)
                        
                if block_changed:
                    builder.start_block(block.id)
                    for i in new_instructions:
                        builder.add_instruction(i)
                else:
                    builder.reuse_block(block)
                    
        return OptimizationResult(builder.new_program, builder.changed, stats)

class CopyPropagationPass(OptimizationPass):
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        # In a fully SSA IR, we'd replace uses of V2 with V1 if V2 = Move(V1).
        # We don't have a Move instruction yet.
        # But we do have: v2 = load v0. If v0 is only stored once...
        # Without SSA and Dominator trees, copy propagation is limited.
        # We will leave this as a no-op for v1.0, to be expanded later.
        return OptimizationResult(program, False, {})

class DeadCodeEliminationPass(OptimizationPass):
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        builder = IRBuilder(program)
        stats = {"removed": 0}
        
        for func in program.functions:
            # Pass 1: Find all used ValueIDs
            used_values = set()
            for block in func.blocks:
                for instr in block.instructions:
                    if isinstance(instr, Load):
                        used_values.add(instr.source_ptr.id)
                    elif isinstance(instr, Store):
                        used_values.add(instr.target_ptr.id)
                        used_values.add(instr.value.id)
                    elif isinstance(instr, BinaryOp):
                        used_values.add(instr.left.id)
                        used_values.add(instr.right.id)
                    elif isinstance(instr, UnaryOp):
                        used_values.add(instr.operand.id)
                    elif isinstance(instr, IntrinsicCall):
                        for arg in instr.args:
                            used_values.add(arg.id)
                    elif isinstance(instr, RuntimeCall):
                        for arg in instr.args:
                            used_values.add(arg.id)
                    elif isinstance(instr, Branch):
                        used_values.add(instr.condition.id)
                    elif isinstance(instr, Return):
                        if instr.value:
                            used_values.add(instr.value.id)
                            
            # Pass 2: Remove pure instructions whose target is never used
            builder.start_function(func.name)
            for block in func.blocks:
                block_changed = False
                new_instructions = []
                
                for instr in block.instructions:
                    # If instruction is pure, and it produces a target, and that target is never used -> DEAD
                    if instr.is_pure and instr.target and instr.target.id not in used_values:
                        block_changed = True
                        builder.mark_changed()
                        stats["removed"] += 1
                        continue
                        
                    new_instructions.append(instr)
                    
                if block_changed:
                    builder.start_block(block.id)
                    for i in new_instructions:
                        builder.add_instruction(i)
                else:
                    builder.reuse_block(block)
                    
        return OptimizationResult(builder.new_program, builder.changed, stats)

class UnreachableBlockRemovalPass(OptimizationPass):
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        builder = IRBuilder(program)
        stats = {"blocks_removed": 0}
        
        for func in program.functions:
            builder.start_function(func.name)
            
            # Find all reachable blocks
            reachable = set()
            if func.blocks:
                reachable.add(func.blocks[0].id.id) # Entry block is always reachable
                
                # Simple BFS
                queue = [func.blocks[0]]
                while queue:
                    current = queue.pop(0)
                    if current.terminator:
                        term = current.terminator
                        if isinstance(term, Jump):
                            if term.target_block.id not in reachable:
                                reachable.add(term.target_block.id)
                                target = next(b for b in func.blocks if b.id.id == term.target_block.id)
                                queue.append(target)
                        elif isinstance(term, Branch):
                            for target_id in (term.true_block.id, term.false_block.id):
                                if target_id not in reachable:
                                    reachable.add(target_id)
                                    target = next(b for b in func.blocks if b.id.id == target_id)
                                    queue.append(target)
            
            func_changed = False
            for block in func.blocks:
                if block.id.id in reachable:
                    builder.reuse_block(block)
                else:
                    func_changed = True
                    builder.mark_changed()
                    stats["blocks_removed"] += 1
                    
        return OptimizationResult(builder.new_program, builder.changed, stats)

class CFGSimplificationPass(OptimizationPass):
    def optimize(self, program: Program, context: CompilationContext) -> OptimizationResult:
        builder = IRBuilder(program)
        stats = {"jumps_threaded": 0, "branches_simplified": 0}
        
        for func in program.functions:
            builder.start_function(func.name)
            
            # Map block_id -> block
            block_map = {b.id.id: b for b in func.blocks}
            
            for block in func.blocks:
                block_changed = False
                new_instructions = []
                
                for instr in block.instructions:
                    if isinstance(instr, Branch):
                        # branch cond ? B : B -> jump B
                        if instr.true_block.id == instr.false_block.id:
                            new_instructions.append(Jump(instr.true_block))
                            block_changed = True
                            builder.mark_changed()
                            stats["branches_simplified"] += 1
                            continue
                            
                    elif isinstance(instr, Jump):
                        # Jump threading
                        target_id = instr.target_block.id
                        if target_id in block_map:
                            target_block = block_map[target_id]
                            # Check if target_block is just a Jump (exactly 1 instruction, which is Jump)
                            if len(target_block.instructions) == 1 and isinstance(target_block.instructions[0], Jump):
                                next_target = target_block.instructions[0].target_block
                                if next_target.id != block.id.id: # Prevent trivial cycle A -> B -> A
                                    new_instructions.append(Jump(next_target))
                                    block_changed = True
                                    builder.mark_changed()
                                    stats["jumps_threaded"] += 1
                                    continue
                    
                    new_instructions.append(instr)
                    
                if block_changed:
                    builder.start_block(block.id)
                    for i in new_instructions:
                        builder.add_instruction(i)
                else:
                    builder.reuse_block(block)
                    
        return OptimizationResult(builder.new_program, builder.changed, stats)
