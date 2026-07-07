from dataclasses import dataclass, field
from compiler.backend.target import TargetBackend
from compiler.backend.register_file import PhysicalRegister
from compiler.backend.allocator.liveness import LivenessResult
from compiler.backend.allocator.intervals import LiveInterval
from compiler.mir.core import VirtualRegister

@dataclass
class AllocationContext:
    target: TargetBackend
    liveness: LivenessResult
    intervals: list[LiveInterval]
    
    # Outputs of the allocation
    # vreg.id -> PhysicalRegister
    register_mapping: dict[int, PhysicalRegister] = field(default_factory=dict)
    
    # vreg.id -> spill slot index
    spill_mapping: dict[int, int] = field(default_factory=dict)
    
    next_spill_slot: int = 0
    
    def allocate_spill_slot(self) -> int:
        idx = self.next_spill_slot
        self.next_spill_slot += 1
        return idx

class LinearScanAllocator:
    def allocate(self, context: AllocationContext):
        # We process intervals sorted by start point
        unhandled = sorted(context.intervals, key=lambda x: x.start)
        active: list[LiveInterval] = []
        
        # Get allocatable physical registers from target
        # For simplicity in this base version, we just lump all GPRs together.
        # A more advanced version would match reg_class.
        from compiler.backend.register_file import RegisterClass
        phys_regs = context.target.register_file().allocatable(RegisterClass.GENERAL_PURPOSE)
        free_regs = set(phys_regs)
        
        for interval in unhandled:
            # 1. Expire old intervals
            active_to_remove = []
            for a in active:
                if a.end <= interval.start:
                    active_to_remove.append(a)
                    if a.assigned_register:
                        free_regs.add(a.assigned_register)
            
            for a in active_to_remove:
                active.remove(a)
                
            # 2. Assign register or spill
            if not free_regs:
                self._spill_at_interval(interval, active, context)
            else:
                # Assign any free register
                reg = free_regs.pop()
                interval.assigned_register = reg
                context.register_mapping[interval.vreg.id] = reg
                active.append(interval)
                
                # Keep active list sorted by end point
                active.sort(key=lambda x: x.end)
                
    def _spill_at_interval(self, current: LiveInterval, active: list[LiveInterval], context: AllocationContext):
        # Heuristic: Farthest next use
        # In this linear scan, the active intervals are sorted by end point.
        # The interval that ends last (which implies farthest next use, simplified) is at the end of active list.
        # Wait, if we want farthest next use, we should actually check `uses` arrays.
        # For now, picking the one that ends the latest (active[-1]) is a classic standard heuristic.
        spill_candidate = active[-1]
        
        if spill_candidate.end > current.end:
            # Spill the candidate, give its register to current
            current.assigned_register = spill_candidate.assigned_register
            context.register_mapping[current.vreg.id] = current.assigned_register
            
            # The candidate is spilled
            spill_candidate.assigned_register = None
            spill_candidate.spilled = True
            context.spill_mapping[spill_candidate.vreg.id] = context.allocate_spill_slot()
            
            # Remove candidate from active, add current
            active.pop()
            active.append(current)
            active.sort(key=lambda x: x.end)
        else:
            # Current interval ends later than all active intervals, spill current
            current.spilled = True
            context.spill_mapping[current.vreg.id] = context.allocate_spill_slot()
