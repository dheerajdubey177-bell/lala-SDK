from dataclasses import dataclass

@dataclass(frozen=True)
class X86Register:
    name: str
    width: int
    id: int # Explicit ID matching the generic PhysicalRegister ID for easy mapping
    
    def __str__(self):
        return self.name

# 64-bit General Purpose Registers
RAX = X86Register("rax", 64, 0)
RBX = X86Register("rbx", 64, 1)
RCX = X86Register("rcx", 64, 2)
RDX = X86Register("rdx", 64, 3)
RSI = X86Register("rsi", 64, 4)
RDI = X86Register("rdi", 64, 5)
RBP = X86Register("rbp", 64, 6)
RSP = X86Register("rsp", 64, 7)
R8  = X86Register("r8", 64, 8)
R9  = X86Register("r9", 64, 9)
R10 = X86Register("r10", 64, 10)
R11 = X86Register("r11", 64, 11)
R12 = X86Register("r12", 64, 12)
R13 = X86Register("r13", 64, 13)
R14 = X86Register("r14", 64, 14)
R15 = X86Register("r15", 64, 15)

ALL_GPRS = [RAX, RBX, RCX, RDX, RSI, RDI, RBP, RSP, R8, R9, R10, R11, R12, R13, R14, R15]
ID_TO_REG = {r.id: r for r in ALL_GPRS}
