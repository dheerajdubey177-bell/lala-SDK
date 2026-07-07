from .opcodes import Opcode
from .machine_ir import X86Register, Immediate, MemoryOperand, LabelOperand

# Allowed shapes for an instruction
# Each shape is a tuple of types.

R = X86Register
I = Immediate
M = MemoryOperand
L = LabelOperand

# Forms are organized by Opcode
ALLOWED_FORMS = {
    Opcode.MOV: [
        (R, R),
        (R, I),
        (R, M),
        (M, R),
        (M, I),
    ],
    Opcode.LEA: [
        (R, M),
    ],
    Opcode.ADD: [
        (R, R),
        (R, I),
        (R, M),
        (M, R),
        (M, I),
    ],
    Opcode.SUB: [
        (R, R),
        (R, I),
        (R, M),
        (M, R),
        (M, I),
    ],
    Opcode.IMUL: [
        (R, R),
        (R, M),
    ],
    Opcode.IDIV: [
        (R,), # Implicit RDX:RAX
        (M,),
    ],
    Opcode.CMP: [
        (R, R),
        (R, I),
        (R, M),
        (M, R),
        (M, I),
    ],
    Opcode.TEST: [
        (R, R),
        (R, I),
        (M, R),
        (M, I),
    ],
    Opcode.JMP: [
        (L,),
    ],
    Opcode.JE: [(L,),],
    Opcode.JNE: [(L,),],
    Opcode.JL: [(L,),],
    Opcode.JLE: [(L,),],
    Opcode.JG: [(L,),],
    Opcode.JGE: [(L,),],
    
    Opcode.CALL: [
        (L,),
        (R,),
    ],
    Opcode.RET: [
        (),
    ],
    Opcode.PUSH: [
        (R,),
        (I,),
        (M,),
    ],
    Opcode.POP: [
        (R,),
        (M,),
    ],
}
