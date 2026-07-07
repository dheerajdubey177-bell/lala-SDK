import unittest
from compiler.mir.core import VirtualRegister, MachineType
from compiler.backend.register_file import RegisterClass, PhysicalRegister, RegisterFile
from compiler.backend.reference_target import ReferenceTarget
from compiler.backend.allocator.intervals import LiveInterval
from compiler.backend.allocator.linear_scan import LinearScanAllocator, AllocationContext
from compiler.backend.allocator.liveness import LivenessResult

class ConstrainedTarget(ReferenceTarget):
    def __init__(self, num_gprs):
        self._regs = [
            PhysicalRegister(id=i, name=f"P{i}", reg_class=RegisterClass.GENERAL_PURPOSE, width=8)
            for i in range(num_gprs)
        ]
    
    def register_file(self):
        return RegisterFile(self._regs)

class TestLinearScan(unittest.TestCase):
    def test_no_spill(self):
        # 3 intervals, 3 registers -> No spills
        target = ConstrainedTarget(3)
        v0 = VirtualRegister(0, MachineType.I64)
        v1 = VirtualRegister(1, MachineType.I64)
        v2 = VirtualRegister(2, MachineType.I64)
        
        i0 = LiveInterval(v0, RegisterClass.GENERAL_PURPOSE, start=0, end=4)
        i1 = LiveInterval(v1, RegisterClass.GENERAL_PURPOSE, start=1, end=3)
        i2 = LiveInterval(v2, RegisterClass.GENERAL_PURPOSE, start=2, end=5)
        
        ctx = AllocationContext(target, LivenessResult(), [i0, i1, i2])
        LinearScanAllocator().allocate(ctx)
        
        # None should be spilled
        self.assertFalse(i0.spilled)
        self.assertFalse(i1.spilled)
        self.assertFalse(i2.spilled)
        
        # They should all have distinct registers
        regs = {i0.assigned_register.id, i1.assigned_register.id, i2.assigned_register.id}
        self.assertEqual(len(regs), 3)
        
    def test_with_spill(self):
        # 3 intervals overlapping, but only 2 registers!
        target = ConstrainedTarget(2)
        v0 = VirtualRegister(0, MachineType.I64)
        v1 = VirtualRegister(1, MachineType.I64)
        v2 = VirtualRegister(2, MachineType.I64)
        
        # i0: [0, 4)
        # i1: [1, 3)
        # i2: [2, 5)
        i0 = LiveInterval(v0, RegisterClass.GENERAL_PURPOSE, start=0, end=4)
        i1 = LiveInterval(v1, RegisterClass.GENERAL_PURPOSE, start=1, end=3)
        i2 = LiveInterval(v2, RegisterClass.GENERAL_PURPOSE, start=2, end=5)
        
        ctx = AllocationContext(target, LivenessResult(), [i0, i1, i2])
        LinearScanAllocator().allocate(ctx)
        
        # By heuristic (farthest end point at time of i2's start = 2):
        # Active at 2: i1 (ends 3), i0 (ends 4). Candidate to spill is i0 (ends 4).
        # i2 ends at 5. Since i0's end (4) < i2's end (5), wait, the active[-1] will be i0 (ends 4).
        # spill_candidate.end (4) > current.end (5)? False. 
        # So it spills `current` (i2) because it ends latest! 
        self.assertFalse(i0.spilled)
        self.assertFalse(i1.spilled)
        self.assertTrue(i2.spilled)
        
        self.assertEqual(ctx.spill_mapping[v2.id], 0)

if __name__ == '__main__':
    unittest.main()
