import unittest
from compiler.mir.core import (
    Function, BasicBlock, BlockID, VirtualRegister, MachineType,
    ConstInstruction, MoveInstruction, BinaryInstruction,
    CompareInstruction, JumpInstruction, BranchInstruction
)
from compiler.backend.allocator.liveness import LivenessAnalyzer

class TestLiveness(unittest.TestCase):
    def test_linear_block(self):
        # b0:
        #   v0 = const 10
        #   v1 = const 20
        #   v2 = add v0, v1
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
        
        analyzer = LivenessAnalyzer()
        res = analyzer.analyze(func)
        
        # v0 and v1 should be live before i3
        self.assertIn(v0, res.instruction_live_before[id(i3)])
        self.assertIn(v1, res.instruction_live_before[id(i3)])
        
        # v2 should be live after i3? No, it's dead since it's never used
        self.assertNotIn(v2, res.instruction_live_after[id(i3)])
        
        # Before i1, nothing is live (live_in for b0 is empty)
        self.assertEqual(len(res.block_live_in[b0.id]), 0)

    def test_loop(self):
        # b0:
        #   v0 = const 0
        #   jmp b1
        # b1:
        #   v1 = const 10
        #   v2 = cmp_lt v0, v1
        #   br v2, b2, b3
        # b2:
        #   v3 = const 1
        #   v0 = add v0, v3
        #   jmp b1
        # b3:
        #   ret v0
        func = Function("loop")
        b0 = BasicBlock(BlockID(0))
        b1 = BasicBlock(BlockID(1))
        b2 = BasicBlock(BlockID(2))
        b3 = BasicBlock(BlockID(3))
        
        v0 = VirtualRegister(0, MachineType.I64)
        v1 = VirtualRegister(1, MachineType.I64)
        v2 = VirtualRegister(2, MachineType.I1)
        v3 = VirtualRegister(3, MachineType.I64)
        
        b0.add(ConstInstruction(v0, 0))
        b0.add(JumpInstruction(b1.id))
        
        b1.add(ConstInstruction(v1, 10))
        b1.add(CompareInstruction(v2, "cmp_lt", v0, v1))
        b1.add(BranchInstruction(v2, b2.id, b3.id))
        
        b2.add(ConstInstruction(v3, 1))
        b2.add(BinaryInstruction(v0, "add", v0, v3))
        b2.add(JumpInstruction(b1.id))
        
        from compiler.mir.core import ReturnInstruction
        b3.add(ReturnInstruction(v0))
        
        func.add_block(b0)
        func.add_block(b1)
        func.add_block(b2)
        func.add_block(b3)
        
        analyzer = LivenessAnalyzer()
        res = analyzer.analyze(func)
        
        # v0 is live_in for b1, b2, and b3
        self.assertIn(v0, res.block_live_in[b1.id])
        self.assertIn(v0, res.block_live_in[b2.id])
        self.assertIn(v0, res.block_live_in[b3.id])
        
        # v0 is NOT live_in for b0 (it's defined there)
        self.assertNotIn(v0, res.block_live_in[b0.id])
        
        # v0 is live_out for b2 (flows back to b1)
        self.assertIn(v0, res.block_live_out[b2.id])

if __name__ == '__main__':
    unittest.main()
