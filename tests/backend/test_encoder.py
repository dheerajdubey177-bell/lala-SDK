import unittest
from compiler.backend.x86_64.machine_ir import MachineInstruction, Immediate, MemoryOperand, LabelOperand
from compiler.backend.x86_64.registers import RAX, RDX, R8, R9, RBP, ID_TO_REG
from compiler.backend.x86_64.opcodes import Opcode
from compiler.backend.x86_64.encoder import MachineEncoder
from compiler.backend.x86_64.addressing import Address

class TestMachineEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = MachineEncoder()
        
    def test_encode_mov_reg_imm32(self):
        instr = MachineInstruction(Opcode.MOV, [RAX, Immediate(10)])
        encoded = self.encoder._encode_instruction(instr)
        self.assertEqual(encoded.bytes_data, b'\x48\xC7\xC0\x0A\x00\x00\x00')
        
    def test_encode_mov_reg_reg(self):
        instr = MachineInstruction(Opcode.MOV, [RAX, RDX])
        encoded = self.encoder._encode_instruction(instr)
        # REX.W (48) + 89 + ModRM (C2)
        self.assertEqual(encoded.bytes_data, b'\x48\x89\xD0')
        
    def test_encode_add_reg_reg(self):
        instr = MachineInstruction(Opcode.ADD, [RAX, RDX])
        encoded = self.encoder._encode_instruction(instr)
        # REX.W (48) + 01 + ModRM (D0)
        self.assertEqual(encoded.bytes_data, b'\x48\x01\xD0')
        
    def test_encode_add_reg_imm(self):
        instr = MachineInstruction(Opcode.ADD, [RAX, Immediate(5)])
        encoded = self.encoder._encode_instruction(instr)
        self.assertEqual(encoded.bytes_data, b'\x48\x81\xC0\x05\x00\x00\x00')

    def test_encode_call(self):
        instr = MachineInstruction(Opcode.CALL, [LabelOperand("get_value")])
        encoded = self.encoder._encode_instruction(instr)
        self.assertEqual(encoded.bytes_data, b'\xE8\x00\x00\x00\x00')
        self.assertEqual(len(encoded.fixups), 1)
        self.assertEqual(encoded.fixups[0].target_label, "get_value")
        self.assertEqual(encoded.fixups[0].offset, 1)

if __name__ == '__main__':
    unittest.main()
