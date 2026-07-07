from enum import Enum, auto

class Opcode(Enum):
    MOV = auto()
    LEA = auto()
    ADD = auto()
    SUB = auto()
    IMUL = auto()
    IDIV = auto()
    CMP = auto()
    TEST = auto()
    JMP = auto()
    JE = auto()
    JNE = auto()
    JL = auto()
    JLE = auto()
    JG = auto()
    JGE = auto()
    CALL = auto()
    RET = auto()
    PUSH = auto()
    POP = auto()
    
    def __str__(self):
        return self.name
