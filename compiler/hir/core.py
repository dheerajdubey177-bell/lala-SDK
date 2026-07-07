from typing import Any
from compiler.semantics.types import Type
from compiler.semantics.intrinsics import IntrinsicID, RuntimeID

class ValueID:
    def __init__(self, id: int):
        self.id = id
        
    def __repr__(self):
        return f"v{self.id}"
        
    def __eq__(self, other):
        return isinstance(other, ValueID) and self.id == other.id
        
    def __hash__(self):
        return hash(self.id)

class BlockID:
    def __init__(self, id: int):
        self.id = id
        
    def __repr__(self):
        return f"b{self.id}"

class Instruction:
    def __init__(self, target: ValueID | None, type: Type | None):
        self.target = target
        self.type = type
        
    @property
    def is_pure(self) -> bool:
        return True
        
    @property
    def reads_memory(self) -> bool:
        return False
        
    @property
    def writes_memory(self) -> bool:
        return False
        
    @property
    def is_terminator(self) -> bool:
        return False

# --- Specific Instructions ---

class Constant(Instruction):
    def __init__(self, target: ValueID, type: Type, value: Any):
        super().__init__(target, type)
        self.value = value
        
    def __repr__(self):
        return f"{self.target} = const {self.type.name} {self.value}"

class Allocate(Instruction):
    # Represents stack allocation for a local variable
    def __init__(self, target: ValueID, type: Type, name: str):
        super().__init__(target, type)
        self.name = name # Original variable name for debug
        
    @property
    def writes_memory(self) -> bool:
        return True # Allocating allocates stack space
        
    @property
    def is_pure(self) -> bool:
        return False

    def __repr__(self):
        return f"{self.target} = alloc {self.type.name} '{self.name}'"

class Load(Instruction):
    def __init__(self, target: ValueID, type: Type, source_ptr: ValueID):
        super().__init__(target, type)
        self.source_ptr = source_ptr
        
    @property
    def reads_memory(self) -> bool:
        return True
        
    def __repr__(self):
        return f"{self.target} = load {self.type.name} {self.source_ptr}"

class Store(Instruction):
    def __init__(self, target_ptr: ValueID, value: ValueID):
        super().__init__(None, None) # Store doesn't produce a value
        self.target_ptr = target_ptr
        self.value = value
        
    @property
    def writes_memory(self) -> bool:
        return True
        
    @property
    def is_pure(self) -> bool:
        return False
        
    def __repr__(self):
        return f"store {self.target_ptr}, {self.value}"

class BinaryOp(Instruction):
    def __init__(self, target: ValueID, type: Type, op: str, left: ValueID, right: ValueID):
        super().__init__(target, type)
        self.op = op
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"{self.target} = {self.op} {self.type.name} {self.left}, {self.right}"

class UnaryOp(Instruction):
    def __init__(self, target: ValueID, type: Type, op: str, operand: ValueID):
        super().__init__(target, type)
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"{self.target} = {self.op} {self.type.name} {self.operand}"

class IntrinsicCall(Instruction):
    def __init__(self, target: ValueID | None, type: Type | None, intrinsic_id: IntrinsicID, args: list[ValueID]):
        super().__init__(target, type)
        self.intrinsic_id = intrinsic_id
        self.args = args
        
    @property
    def is_pure(self) -> bool:
        return False # PRINT, INPUT etc have side effects
        
    def __repr__(self):
        tgt = f"{self.target} = " if self.target else ""
        return f"{tgt}intrinsic {self.intrinsic_id.name}({', '.join(map(str, self.args))})"

class RuntimeCall(Instruction):
    def __init__(self, target: ValueID | None, type: Type | None, runtime_id: RuntimeID, args: list[ValueID], side_effects: bool=True, pure: bool=False):
        super().__init__(target, type)
        self.runtime_id = runtime_id
        self.args = args
        self._pure = pure
        
    @property
    def is_pure(self) -> bool:
        return self._pure
        
    def __repr__(self):
        tgt = f"{self.target} = " if self.target else ""
        return f"{tgt}runtime {self.runtime_id.name}({', '.join(map(str, self.args))})"

# --- Terminators ---

class Terminator(Instruction):
    def __init__(self):
        super().__init__(None, None)
        
    @property
    def is_terminator(self) -> bool:
        return True
        
    @property
    def is_pure(self) -> bool:
        return False # Terminators alter control flow

class Jump(Terminator):
    def __init__(self, target_block: BlockID):
        super().__init__()
        self.target_block = target_block
        
    def __repr__(self):
        return f"jump {self.target_block}"

class Branch(Terminator):
    def __init__(self, condition: ValueID, true_block: BlockID, false_block: BlockID):
        super().__init__()
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
        
    def __repr__(self):
        return f"branch {self.condition} ? {self.true_block} : {self.false_block}"

class Return(Terminator):
    def __init__(self, value: ValueID | None):
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
class Call(Instruction):
    def __init__(self, target: ValueID, type, func_name: str, arguments: list[ValueID]):
        super().__init__(target, type)
        self.func_name = func_name
        self.arguments = arguments

    def __repr__(self):
        args_str = ', '.join(map(str, self.arguments))
        t = f'{self.target} = ' if self.target else ''
        return f'{t}call {self.func_name}({args_str})'
