import unittest
from compiler.mir.core import (
    Function, BasicBlock, BlockID, VirtualRegister, MachineType,
    ConstInstruction, BinaryInstruction, MoveInstruction
)
from compiler.backend.reference_target import ReferenceTarget
from compiler.backend.allocator.liveness import LivenessAnalyzer
from compiler.backend.allocator.intervals import IntervalBuilder
from compiler.backend.allocator.linear_scan import LinearScanAllocator, AllocationContext
from compiler.backend.allocator.spiller import SpillInsertionPass
from compiler.backend.allocator.pmir_builder import PMIRBuilder
from compiler.backend.allocator.validator import PMIRValidator

class TestFullPipeline(unittest.TestCase):
    def test_pipeline_no_spill(self):
        func = Function("test")
        b0 = BasicBlock(BlockID(0))
        
        v0 = VirtualRegister(0, MachineType.I64)
        v1 = VirtualRegister(1, MachineType.I64)
        v2 = VirtualRegister(2, MachineType.I64)
        
        b0.add(ConstInstruction(v0, 10))
        b0.add(ConstInstruction(v1, 20))
        b0.add(BinaryInstruction(v2, "add", v0, v1))
        
        # We need a terminator to pass validation
        from compiler.mir.core import ReturnInstruction
        b0.add(ReturnInstruction(v2))
        func.add_block(b0)
        
        target = ReferenceTarget() # Has 8 GPRs, plenty
        liveness = LivenessAnalyzer().analyze(func)
        intervals = IntervalBuilder().build(func, liveness)
        
        ctx = AllocationContext(target, liveness, intervals)
        LinearScanAllocator().allocate(ctx)
        
        func_spilled = SpillInsertionPass(ctx).run(func)
        pmir_func = PMIRBuilder(ctx).build(func_spilled)
        
        validator = PMIRValidator(target)
        validator.validate(pmir_func) # Should not raise
        
        # Check that pmir_func has PhysicalRegisters
        term = pmir_func.blocks[0].terminator
        from compiler.backend.register_file import PhysicalRegister
        self.assertIsInstance(term.value, PhysicalRegister)

if __name__ == '__main__':
    unittest.main()
