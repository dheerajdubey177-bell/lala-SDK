from dataclasses import dataclass, field
from compiler.mir.core import VirtualRegister, Function
from compiler.backend.register_file import RegisterClass, PhysicalRegister
from .liveness import LivenessAnalyzer, LivenessResult, _get_def_use

@dataclass
class LiveInterval:
    vreg: VirtualRegister
    reg_class: RegisterClass
    start: int
    end: int
    uses: list[int] = field(default_factory=list)
    definition: int = -1
    spilled: bool = False
    assigned_register: PhysicalRegister | None = None
    
    def overlaps(self, other: 'LiveInterval') -> bool:
        return not (self.end <= other.start or other.end <= self.start)

class IntervalBuilder:
    def build(self, func: Function, liveness: LivenessResult) -> list[LiveInterval]:
        intervals: dict[VirtualRegister, LiveInterval] = {}
        
        # 1. Assign linear indices to instructions
        instr_indices = {}
        current_idx = 0
        
        for block in func.blocks:
            # We assume blocks are in some topological order for good linear indices
            for instr in block.instructions:
                instr_indices[id(instr)] = current_idx
                current_idx += 1
                
        # 2. Iterate backwards to accurately compute start/end ranges
        for block in reversed(func.blocks):
            # All variables live out of the block extend to at least the end of this block
            block_end_idx = instr_indices[id(block.instructions[-1])] if block.instructions else current_idx
            
            for vreg in liveness.block_live_out[block.id]:
                if vreg not in intervals:
                    # Default class is GPR for now
                    intervals[vreg] = LiveInterval(vreg, RegisterClass.GENERAL_PURPOSE, start=0, end=block_end_idx)
                else:
                    intervals[vreg].end = max(intervals[vreg].end, block_end_idx)
            
            for instr in reversed(block.instructions):
                idx = instr_indices[id(instr)]
                defs, uses = _get_def_use(instr)
                
                # When a def is encountered, its interval start is this instruction
                for d in defs:
                    if d not in intervals:
                        intervals[d] = LiveInterval(d, RegisterClass.GENERAL_PURPOSE, start=idx, end=idx)
                    else:
                        intervals[d].start = idx
                    intervals[d].definition = idx
                    
                # When a use is encountered, its interval must extend to this instruction
                for u in uses:
                    if u not in intervals:
                        intervals[u] = LiveInterval(u, RegisterClass.GENERAL_PURPOSE, start=0, end=idx)
                    else:
                        intervals[u].end = max(intervals[u].end, idx)
                    intervals[u].uses.append(idx)
                    
        # Sort uses and return intervals sorted by start time
        result = list(intervals.values())
        for r in result:
            r.uses.sort()
        result.sort(key=lambda x: x.start)
        
        return result
