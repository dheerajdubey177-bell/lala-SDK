import unittest
from compiler.mir.core import (
    Function, BasicBlock, BlockID, VirtualRegister, MachineType,
    ConstInstruction, BinaryInstruction
)
from compiler.backend.allocator.liveness import LivenessAnalyzer
from compiler.backend.allocator.intervals import IntervalBuilder

class TestIntervals(unittest.TestCase):
    def test_interval_construction(self):
        # b0:
        # 0: v0 = const 10
        # 1: v1 = const 20
        # 2: v2 = add v0, v1
        func = Function("test")
        b0 = BasicBlock(BlockID(0))
        
        v0 = VirtualRegister(0, MachineType.I64)
        v1 = VirtualRegister(1, MachineType.I64)
        v2 = VirtualRegister(2, MachineType.I64)
        
        i1 = ConstInstruction(v0, 10)
        i2 = ConstInstruction(v1, 20)
        i3 = BinaryInstruction(v2, "add", v0, v1)
        
        b0.add(i1)
        b0.add(i2)
        b0.add(i3)
        func.add_block(b0)
        
        liveness = LivenessAnalyzer().analyze(func)
        intervals = IntervalBuilder().build(func, liveness)
        
        self.assertEqual(len(intervals), 3)
        
        # Intervals are sorted by start index
        int_v0 = intervals[0]
        self.assertEqual(int_v0.vreg.id, 0)
        self.assertEqual(int_v0.start, 0)
        self.assertEqual(int_v0.end, 2) # Ends exactly at use index 2
        self.assertEqual(int_v0.definition, 0)
        self.assertEqual(int_v0.uses, [2])
        
        int_v1 = intervals[1]
        self.assertEqual(int_v1.vreg.id, 1)
        self.assertEqual(int_v1.start, 1)
        self.assertEqual(int_v1.end, 2)
        self.assertEqual(int_v1.definition, 1)
        self.assertEqual(int_v1.uses, [2])
        
        int_v2 = intervals[2]
        self.assertEqual(int_v2.vreg.id, 2)
        self.assertEqual(int_v2.start, 2)
        self.assertEqual(int_v2.end, 2) # Ends immediately since it's never used
        self.assertEqual(int_v2.definition, 2)
        self.assertEqual(int_v2.uses, [])
        
        self.assertTrue(int_v0.overlaps(int_v1))
        self.assertFalse(int_v0.overlaps(int_v2))

if __name__ == '__main__':
    unittest.main()
