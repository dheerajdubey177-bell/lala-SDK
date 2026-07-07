from .machine_ir import MachineProgram, MachineInstruction, MachineOperand, Immediate, MemoryOperand, LabelOperand, MachineFunction, MachineBlock
from .registers import X86Register
from .opcodes import Opcode
from .code_image import CodeImage, EncodedFunction, EncodedBlock, EncodedInstruction, Fixup, FixupKind
from .encoder_validator import EncoderValidator
import struct

HW_REG_ID = {
    0: 0,  # RAX
    1: 3,  # RBX
    2: 1,  # RCX
    3: 2,  # RDX
    4: 6,  # RSI
    5: 7,  # RDI
    6: 5,  # RBP
    7: 4,  # RSP
    8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15
}

class MachineEncoder:
    def __init__(self):
        self.validator = EncoderValidator()

    def encode(self, program: MachineProgram) -> CodeImage:
        functions = []
        for func in program.functions:
            functions.append(self._encode_function(func))
            
        # Compute offsets and concatenate bytes
        image_bytes = bytearray()
        fixups = []
        current_offset = 0
        
        for func in functions:
            func.offset = current_offset
            for block in func.blocks:
                block.offset = current_offset
                for instr in block.instructions:
                    instr.offset = current_offset
                    image_bytes.extend(instr.bytes_data)
                    for f in instr.fixups:
                        f.offset = current_offset + f.offset # Make fixup absolute to image
                        fixups.append(f)
                    current_offset += instr.length
                block.length = current_offset - block.offset
            func.length = current_offset - func.offset
            
        return CodeImage(functions=functions, bytes_data=bytes(image_bytes), fixups=fixups)

    def _encode_function(self, func: MachineFunction) -> EncodedFunction:
        blocks = [self._encode_block(b) for b in func.blocks]
        return EncodedFunction(func.name, blocks, b'', 0, 0)

    def _encode_block(self, block: MachineBlock) -> EncodedBlock:
        instructions = []
        for instr in block.instructions:
            self.validator.validate(instr)
            instructions.append(self._encode_instruction(instr))
        return EncodedBlock(block.name, instructions, b'', 0, 0)

    def _encode_instruction(self, instr: MachineInstruction) -> EncodedInstruction:
        buffer = bytearray()
        fixups = []
        
        if instr.opcode == Opcode.RET:
            buffer.append(0xC3)
            
        elif instr.opcode == Opcode.MOV:
            dst = instr.operands[0]
            src = instr.operands[1]
            if isinstance(dst, X86Register) and isinstance(src, Immediate):
                # MOV reg, imm32 (C7 /0 id)
                # For 64-bit imm, it is B8+r
                buffer.extend(self._encode_rex(dst, None, True))
                if -2147483648 <= src.value <= 2147483647:
                    buffer.append(0xC7)
                    buffer.append(self._modrm(0b11, 0, HW_REG_ID[dst.id]))
                    buffer.extend(struct.pack("<i", src.value))
                else:
                    buffer.append(0xB8 + (HW_REG_ID[dst.id] & 7))
                    buffer.extend(struct.pack("<q", src.value))
            elif isinstance(dst, X86Register) and isinstance(src, X86Register):
                buffer.extend(self._encode_rex(dst, src, True))
                buffer.append(0x89)
                buffer.append(self._modrm(0b11, HW_REG_ID[src.id], HW_REG_ID[dst.id]))
            elif isinstance(dst, MemoryOperand) and isinstance(src, X86Register):
                buffer.extend(self._encode_rex(dst.address.base, src, True))
                buffer.append(0x89)
                buffer.append(self._modrm(0b01, HW_REG_ID[src.id], HW_REG_ID[dst.address.base.id]))
                buffer.append(dst.address.displacement & 0xFF) # simple 8-bit disp for now
            elif isinstance(dst, X86Register) and isinstance(src, MemoryOperand):
                buffer.extend(self._encode_rex(dst, src.address.base, True))
                buffer.append(0x8B)
                buffer.append(self._modrm(0b01, HW_REG_ID[dst.id], HW_REG_ID[src.address.base.id]))
                buffer.append(src.address.displacement & 0xFF) # simple 8-bit disp for now
            else:
                raise NotImplementedError(f"Unsupported MOV operands: {dst}, {src}")
                
        elif instr.opcode in (Opcode.ADD, Opcode.SUB, Opcode.CMP):
            opc = {Opcode.ADD: 0x01, Opcode.SUB: 0x29, Opcode.CMP: 0x39}[instr.opcode]
            dst, src = instr.operands
            if isinstance(dst, X86Register) and isinstance(src, X86Register):
                buffer.extend(self._encode_rex(dst, src, True))
                buffer.append(opc)
                buffer.append(self._modrm(0b11, HW_REG_ID[src.id], HW_REG_ID[dst.id]))
            elif isinstance(dst, X86Register) and isinstance(src, Immediate):
                # 81 /0 id for ADD, 81 /5 id for SUB, 81 /7 id for CMP
                ext = {Opcode.ADD: 0, Opcode.SUB: 5, Opcode.CMP: 7}[instr.opcode]
                buffer.extend(self._encode_rex(dst, None, True))
                buffer.append(0x81)
                buffer.append(self._modrm(0b11, ext, HW_REG_ID[dst.id]))
                buffer.extend(struct.pack("<i", src.value))
                
        elif instr.opcode == Opcode.IMUL:
            dst, src = instr.operands
            buffer.extend(self._encode_rex(dst, src, True))
            buffer.extend([0x0F, 0xAF])
            buffer.append(self._modrm(0b11, HW_REG_ID[dst.id], HW_REG_ID[src.id]))
            
        elif instr.opcode == Opcode.IDIV:
            src = instr.operands[0]
            buffer.extend(self._encode_rex(src, None, True))
            buffer.append(0xF7)
            buffer.append(self._modrm(0b11, 7, HW_REG_ID[src.id]))
            
        elif instr.opcode == Opcode.CALL:
            buffer.append(0xE8)
            fixups.append(Fixup(len(buffer), FixupKind.REL32, instr.operands[0].name))
            buffer.extend(b'\x00\x00\x00\x00')
            
        elif instr.opcode == Opcode.JMP:
            buffer.append(0xE9)
            fixups.append(Fixup(len(buffer), FixupKind.REL32, instr.operands[0].name))
            buffer.extend(b'\x00\x00\x00\x00')
            
        elif instr.opcode in (Opcode.JE, Opcode.JNE, Opcode.JL, Opcode.JLE, Opcode.JG, Opcode.JGE):
            opc = {Opcode.JE: 0x84, Opcode.JNE: 0x85, Opcode.JL: 0x8C, Opcode.JLE: 0x8E, Opcode.JG: 0x8F, Opcode.JGE: 0x8D}[instr.opcode]
            buffer.extend([0x0F, opc])
            fixups.append(Fixup(len(buffer), FixupKind.REL32, instr.operands[0].name))
            buffer.extend(b'\x00\x00\x00\x00')
            
        else:
            raise NotImplementedError(f"Encoding not implemented for {instr.opcode}")
            
        return EncodedInstruction(instr, bytes(buffer), 0, len(buffer), fixups)

    def _encode_rex(self, rm_reg, reg_reg, w: bool) -> bytes:
        rex = 0x40
        if w: rex |= 0x08
        if reg_reg and HW_REG_ID[reg_reg.id] > 7: rex |= 0x04
        if rm_reg and HW_REG_ID[rm_reg.id] > 7: rex |= 0x01
        return bytes([rex]) if rex != 0x40 else b''

    def _modrm(self, mod: int, reg: int, rm: int) -> int:
        return ((mod & 3) << 6) | ((reg & 7) << 3) | (rm & 7)
