from dataclasses import dataclass
from .opcodes import Opcode

@dataclass
class EncodingDescriptor:
    opcode_bytes: list[int]
    has_modrm: bool = False
    modrm_extension: int | None = None
    immediate_size: int = 0

# A minimal mapping for the opcodes we need.
# X86-64 has a massive matrix, we just encode what InstructionSelector emits.
OPCODE_MAP = {
    Opcode.MOV: EncodingDescriptor([0x89], has_modrm=True), # Default reg-to-reg/mem MOV
    Opcode.ADD: EncodingDescriptor([0x01], has_modrm=True),
    Opcode.SUB: EncodingDescriptor([0x29], has_modrm=True),
    Opcode.RET: EncodingDescriptor([0xC3]),
    Opcode.CALL: EncodingDescriptor([0xE8], immediate_size=4),
}
