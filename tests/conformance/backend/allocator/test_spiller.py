import unittest
from compiler.mir.core import (
    Function, BasicBlock, BlockID, VirtualRegister, MachineType,
    ConstInstruction, BinaryInstruction, MoveInstruction
)
from compiler.backend.allocator.linear_scan import AllocationContext
from compiler.backend.allocator.spiller import SpillInsertionPass
from compiler.backend.reference_target import ReferenceTarget

class TestSpiller(unittest.TestCase):
    def test_spill_insertion(self):
        func = Function("test")
        b0 = BasicBlock(BlockID(0))
        
        v0 = VirtualRegister(0, MachineType.I64)
        v1 = VirtualRegister(1, MachineType.I64)
        v2 = VirtualRegister(2, MachineType.I64)
        
        b0.add(ConstInstruction(v0, 10))
        b0.add(ConstInstruction(v1, 20))
        b0.add(BinaryInstruction(v2, "add", v0, v1))
        b0.add(MoveInstruction(v0, v2))
        
        func.add_block(b0)
        
        ctx = AllocationContext(ReferenceTarget(), None, [])
        ctx.spill_mapping = {0: 42} # v0 is spilled to stack slot 42
        
        spiller = SpillInsertionPass(ctx)
        new_func = spiller.run(func)
        
        instrs = new_func.blocks[0].instructions
        
        # 0: v0_temp_def = const 10
        # 1: store stack42, v0_temp_def
        # 2: v1 = const 20
        # 3: v0_temp_use = load stack42
        # 4: v2 = add v0_temp_use, v1
        # 5: v0_temp_def2 = mov v2
        # 6: store stack42, v0_temp_def2
        
        self.assertEqual(len(instrs), 7)
        
        from compiler.mir.core import StoreInstruction, LoadInstruction
        self.assertIsInstance(instrs[1], StoreInstruction)
        self.assertEqual(instrs[1].target_ptr.id, 42)
        
        self.assertIsInstance(instrs[3], LoadInstruction)
        self.assertEqual(instrs[3].source_ptr.id, 42)

if __name__ == '__main__':
    unittest.main()
