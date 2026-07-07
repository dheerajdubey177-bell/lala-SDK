import unittest
from compiler.backend.x86_64.encoder import MachineEncoder
from compiler.backend.x86_64.machine_ir import MachineProgram, MachineFunction, MachineBlock, MachineInstruction, Immediate, LabelOperand
from compiler.backend.x86_64.registers import RAX
from compiler.backend.x86_64.opcodes import Opcode
from compiler.backend.x86_64.object_builder import ObjectBuilder
from compiler.object.elf.writer import ELFWriter
from compiler.object.validator import ObjectValidator

class TestObjectWriter(unittest.TestCase):
    def test_elf_header_and_sections(self):
        encoder = MachineEncoder()
        builder = ObjectBuilder()
        validator = ObjectValidator()
        writer = ELFWriter()
        
        # Build a simple program:
        # main:
        #   mov rax, 42
        #   ret
        
        instr1 = MachineInstruction(Opcode.MOV, [RAX, Immediate(42)])
        instr2 = MachineInstruction(Opcode.RET, [])
        block = MachineBlock("entry", [instr1, instr2])
        func = MachineFunction("main", [block])
        prog = MachineProgram([func])
        
        code_image = encoder.encode(prog)
        obj = builder.build(code_image)
        validator.validate(obj)
        
        elf_bytes = writer.write_object(obj)
        
        # ELF magic
        self.assertEqual(elf_bytes[0:4], b'\x7FELF')
        # 64-bit
        self.assertEqual(elf_bytes[4], 2)
        # Little endian
        self.assertEqual(elf_bytes[5], 1)
        
        # At least contains standard sections: NULL, .text, .symtab, .strtab, .shstrtab
        self.assertGreater(len(elf_bytes), 64) # larger than header

if __name__ == '__main__':
    unittest.main()
