import unittest
from compiler.mir.core import (
    Function, BasicBlock, BlockID, VirtualRegister, MachineType, StackSlot,
    ConstInstruction, BinaryInstruction, ReturnInstruction
)
from compiler.backend.register_file import PhysicalRegister, RegisterClass
from compiler.backend.x86_64.registers import RAX, RCX
from compiler.backend.x86_64.selector import InstructionSelector
from compiler.backend.x86_64.printer import IntelAssemblyPrinter
from compiler.backend.x86_64.validator import MachineValidator, MachineValidationError

class TestX86CodeGen(unittest.TestCase):
    def test_basic_arithmetic(self):
        func = Function("test_arithmetic")
        b0 = BasicBlock(BlockID(0))
        
        # We manually construct a PMIR function to feed to the Selector
        # Normally this comes from PMIRBuilder
        
        p_rax = PhysicalRegister(RAX.id, RAX.name, RegisterClass.GENERAL_PURPOSE, 64)
        p_rcx = PhysicalRegister(RCX.id, RCX.name, RegisterClass.GENERAL_PURPOSE, 64)
        
        b0.add(ConstInstruction(p_rcx, 10))
        b0.add(BinaryInstruction(p_rax, "add", p_rax, p_rcx)) # RAX = RAX + RCX
        b0.add(ReturnInstruction(None))
        
        func.add_block(b0)
        
        selector = InstructionSelector()
        mfunc = selector.select_function(func)
        
        validator = MachineValidator()
        validator.validate(mfunc)
        
        printer = IntelAssemblyPrinter()
        asm = printer.print_function(mfunc)
        
        # Expecting:
        # .intel_syntax noprefix
        # .globl test_arithmetic
        # test_arithmetic:
        # .L0:
        #     mov rcx, 10
        #     add rax, rcx
        #     ret
        
        self.assertIn("mov rcx, 10", asm)
        self.assertIn("add rax, rcx", asm)
        self.assertIn("ret", asm)
        
    def test_validation_failure_mem_to_mem(self):
        from compiler.backend.x86_64.machine_ir import MachineFunction, MachineBlock, MachineInstruction
        from compiler.backend.x86_64.opcodes import Opcode
        from compiler.backend.x86_64.addressing import Address
        from compiler.backend.x86_64.machine_ir import MemoryOperand
        
        mfunc = MachineFunction("bad_func", [
            MachineBlock(".L0", [
                MachineInstruction(Opcode.ADD, [
                    MemoryOperand(Address(base=RAX)),
                    MemoryOperand(Address(base=RCX))
                ])
            ])
        ])
        
        validator = MachineValidator()
        with self.assertRaises(MachineValidationError):
            validator.validate(mfunc)

if __name__ == '__main__':
    unittest.main()
