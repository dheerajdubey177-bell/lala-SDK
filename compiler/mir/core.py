from enum import Enum, auto
from typing import Any

class MachineType(Enum):
    I1 = "i1"
    I8 = "i8"
    I16 = "i16"
    I32 = "i32"
    I64 = "i64"
    F32 = "f32"
    F64 = "f64"
    PTR = "ptr"

class VirtualRegister:
    def __init__(self, id: int, type: MachineType):
        self.id = id
        self.type = type
        
    def __repr__(self):
        return f"v{self.id}:{self.type.value}"
        
    def __eq__(self, other):
        return isinstance(other, VirtualRegister) and self.id == other.id
        
    def __hash__(self):
        return hash(self.id)

class StackSlot:
    def __init__(self, id: int):
        self.id = id
        self.type = MachineType.PTR
        
    def __repr__(self):
        return f"stack{self.id}:{self.type.value}"

class BlockID:
    def __init__(self, id: int):
        self.id = id
        
    def __repr__(self):
        return f"b{self.id}"

from typing import Any, Generic, TypeVar

R = TypeVar("R")
M = TypeVar("M")

class Instruction(Generic[R, M]):
    pass

# --- Instructions ---

class ConstInstruction(Instruction[R, M]):
    def __init__(self, target: R, value: Any):
        super().__init__()
        self.target = target
        self.value = value

    def __repr__(self):
        return f"{self.target} = const {self.value}"

class MoveInstruction(Instruction[R, M]):
    def __init__(self, target: R, source: R):
        super().__init__()
        self.target = target
        self.source = source
        
    def __repr__(self):
        return f"{self.target} = mov {self.source}"

class BinaryInstruction(Instruction[R, M]):
    def __init__(self, target: R, op: str, left: R, right: R):
        super().__init__()
        self.target = target
        self.op = op # "add", "sub", "mul", "div", "rem", "and", "or", "xor"
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"{self.target} = {self.op} {self.left}, {self.right}"

class UnaryInstruction(Instruction[R, M]):
    def __init__(self, target: R, op: str, operand: R):
        super().__init__()
        self.target = target
        self.op = op # "not"
        self.operand = operand
        
    def __repr__(self):
        return f"{self.target} = {self.op} {self.operand}"

class CompareInstruction(Instruction[R, M]):
    def __init__(self, target: R, op: str, left: R, right: R):
        super().__init__()
        self.target = target # Always I1
        self.op = op # "cmp_eq", "cmp_ne", "cmp_lt", "cmp_le", "cmp_gt", "cmp_ge"
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"{self.target} = {self.op} {self.left}, {self.right}"

class LoadInstruction(Instruction[R, M]):
    def __init__(self, target: R, source_ptr: R | M):
        super().__init__()
        self.target = target
        self.source_ptr = source_ptr
        
    def __repr__(self):
        return f"{self.target} = load {self.source_ptr}"

class StoreInstruction(Instruction[R, M]):
    def __init__(self, target_ptr: R | M, source: R):
        super().__init__()
        self.target_ptr = target_ptr
        self.source = source
        
    def __repr__(self):
        return f"store {self.target_ptr}, {self.source}"

# --- Calling Convention ---

class SetArgInstruction(Instruction[R, M]):
    def __init__(self, index: int, value: R):
        super().__init__()
        self.index = index
        self.value = value
        
    def __repr__(self):
        return f"arg{self.index} = {self.value}"

class CallInstruction(Instruction[R, M]):
    def __init__(self, func_name: str):
        super().__init__()
        self.func_name = func_name
        
    def __repr__(self):
        return f"call {self.func_name}"

class GetRetvalInstruction(Instruction[R, M]):
    def __init__(self, target: R):
        super().__init__()
        self.target = target
        
    def __repr__(self):
        return f"{self.target} = retval"

# --- Terminators ---

class Terminator(Instruction[R, M]):
    pass

class JumpInstruction(Terminator[R, M]):
    def __init__(self, target_block: BlockID):
        super().__init__()
        self.target_block = target_block
        
    def __repr__(self):
        return f"jmp {self.target_block}"

class BranchInstruction(Terminator[R, M]):
    def __init__(self, condition: R, true_block: BlockID, false_block: BlockID):
        super().__init__()
        self.condition = condition # Expected I1
        self.true_block = true_block
        self.false_block = false_block
        
    def __repr__(self):
        return f"br {self.condition}, {self.true_block}, {self.false_block}"

class ReturnInstruction(Terminator[R, M]):
    def __init__(self, value: R | None):
        super().__init__()
        self.value = value
        
    def __repr__(self):
        return f"ret {self.value}" if self.value else "ret"

# --- Structures ---

class BasicBlock:
    def __init__(self, id: BlockID):
        self.id = id
        self.instructions: list[Instruction] = []
        
    def add(self, instr: Instruction):
        self.instructions.append(instr)
        
    @property
    def terminator(self) -> Terminator | None:
        if self.instructions and isinstance(self.instructions[-1], Terminator):
            return self.instructions[-1]
        return None

class Function:
    def __init__(self, name: str):
        self.name = name
        self.blocks: list[BasicBlock] = []
        
    def add_block(self, block: BasicBlock):
        self.blocks.append(block)

class Program:
    def __init__(self):
        self.functions: list[Function] = []
