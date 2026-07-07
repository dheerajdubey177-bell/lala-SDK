from dataclasses import dataclass, field
from compiler.mir.core import (
    Function, BasicBlock, Instruction, Terminator,
    JumpInstruction, BranchInstruction, ReturnInstruction,
    ConstInstruction, MoveInstruction, BinaryInstruction, UnaryInstruction,
    CompareInstruction, LoadInstruction, StoreInstruction,
    SetArgInstruction, CallInstruction, GetRetvalInstruction,
    VirtualRegister, BlockID
)

@dataclass
class LivenessResult:
    block_live_in: dict[BlockID, set[VirtualRegister]] = field(default_factory=dict)
    block_live_out: dict[BlockID, set[VirtualRegister]] = field(default_factory=dict)
    
    # Map from instruction object identity (id()) to its live sets
    instruction_live_before: dict[int, set[VirtualRegister]] = field(default_factory=dict)
    instruction_live_after: dict[int, set[VirtualRegister]] = field(default_factory=dict)

def _get_successors(block: BasicBlock, func: Function) -> list[BasicBlock]:
    term = block.terminator
    if isinstance(term, JumpInstruction):
        return [b for b in func.blocks if b.id.id == term.target_block.id]
    elif isinstance(term, BranchInstruction):
        return [b for b in func.blocks if b.id.id in (term.true_block.id, term.false_block.id)]
    elif isinstance(term, ReturnInstruction):
        return []
    return []

def _get_def_use(instr: Instruction) -> tuple[set[VirtualRegister], set[VirtualRegister]]:
    """Returns (defs, uses) for an instruction."""
    defs = set()
    uses = set()
    
    if isinstance(instr, ConstInstruction):
        if isinstance(instr.target, VirtualRegister): defs.add(instr.target)
    elif isinstance(instr, MoveInstruction):
        if isinstance(instr.target, VirtualRegister): defs.add(instr.target)
        if isinstance(instr.source, VirtualRegister): uses.add(instr.source)
    elif isinstance(instr, BinaryInstruction) or isinstance(instr, CompareInstruction):
        if isinstance(instr.target, VirtualRegister): defs.add(instr.target)
        if isinstance(instr.left, VirtualRegister): uses.add(instr.left)
        if isinstance(instr.right, VirtualRegister): uses.add(instr.right)
    elif isinstance(instr, UnaryInstruction):
        if isinstance(instr.target, VirtualRegister): defs.add(instr.target)
        if isinstance(instr.operand, VirtualRegister): uses.add(instr.operand)
    elif isinstance(instr, LoadInstruction):
        if isinstance(instr.target, VirtualRegister): defs.add(instr.target)
        if isinstance(instr.source_ptr, VirtualRegister): uses.add(instr.source_ptr)
    elif isinstance(instr, StoreInstruction):
        if isinstance(instr.target_ptr, VirtualRegister): uses.add(instr.target_ptr)
        if isinstance(instr.source, VirtualRegister): uses.add(instr.source)
    elif isinstance(instr, SetArgInstruction):
        if isinstance(instr.value, VirtualRegister): uses.add(instr.value)
    elif isinstance(instr, CallInstruction):
        pass
    elif isinstance(instr, GetRetvalInstruction):
        if isinstance(instr.target, VirtualRegister): defs.add(instr.target)
    elif isinstance(instr, BranchInstruction):
        if isinstance(instr.condition, VirtualRegister): uses.add(instr.condition)
    elif isinstance(instr, ReturnInstruction):
        if instr.value and isinstance(instr.value, VirtualRegister): uses.add(instr.value)
        
    return defs, uses

class LivenessAnalyzer:
    def analyze(self, func: Function) -> LivenessResult:
        result = LivenessResult()
        
        # Initialize block sets
        for b in func.blocks:
            result.block_live_in[b.id] = set()
            result.block_live_out[b.id] = set()
            
        changed = True
        while changed:
            changed = False
            # Iterate backwards
            for block in reversed(func.blocks):
                # 1. live_out[B] = Union(live_in[S] for S in successors)
                new_live_out = set()
                for succ in _get_successors(block, func):
                    new_live_out.update(result.block_live_in[succ.id])
                    
                result.block_live_out[block.id] = new_live_out
                
                # 2. Compute live_in[B] by walking instructions backwards
                live = set(new_live_out)
                for instr in reversed(block.instructions):
                    defs, uses = _get_def_use(instr)
                    result.instruction_live_after[id(instr)] = set(live)
                    
                    # live_before = uses U (live_after - defs)
                    live.difference_update(defs)
                    live.update(uses)
                    
                    result.instruction_live_before[id(instr)] = set(live)
                    
                new_live_in = live
                if new_live_in != result.block_live_in[block.id]:
                    result.block_live_in[block.id] = new_live_in
                    changed = True
                    
        return result
