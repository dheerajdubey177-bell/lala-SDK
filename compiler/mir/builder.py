from typing import Any
from .core import *

class MIRBuilder:
    def __init__(self):
        self.program = Program()
        self.current_function = None
        self.current_block = None
        
        self.next_vreg_id = 0
        self.next_stack_slot_id = 0
        self.next_block_id = 0
        
    def start_function(self, name: str):
        self.current_function = Function(name)
        self.program.functions.append(self.current_function)
        
        # Reset IDs per function for cleaner MIR (optional, but good practice)
        self.next_vreg_id = 0
        self.next_stack_slot_id = 0
        self.next_block_id = 0
        
    def start_block(self, block_id: BlockID | None = None) -> BlockID:
        if block_id is None:
            block_id = BlockID(self.next_block_id)
            self.next_block_id += 1
            
        self.current_block = BasicBlock(block_id)
        if self.current_function:
            self.current_function.add_block(self.current_block)
        return block_id
        
    def _next_vreg(self, type: MachineType) -> VirtualRegister:
        reg = VirtualRegister(self.next_vreg_id, type)
        self.next_vreg_id += 1
        return reg

    def alloc_stack_slot(self) -> StackSlot:
        slot = StackSlot(self.next_stack_slot_id)
        self.next_stack_slot_id += 1
        return slot

    def const(self, type: MachineType, value: Any) -> VirtualRegister:
        target = self._next_vreg(type)
        self.current_block.add(ConstInstruction(target, value))
        return target
        
    def mov(self, source: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(source.type)
        self.current_block.add(MoveInstruction(target, source))
        return target
        
    def add(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "add", left, right))
        return target
        
    def sub(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "sub", left, right))
        return target
        
    def mul(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "mul", left, right))
        return target
        
    def div(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "div", left, right))
        return target
        
    def rem(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "rem", left, right))
        return target
        
    def bit_and(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "and", left, right))
        return target
        
    def bit_or(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "or", left, right))
        return target
        
    def bit_xor(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(left.type)
        self.current_block.add(BinaryInstruction(target, "xor", left, right))
        return target
        
    def bit_not(self, operand: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(operand.type)
        self.current_block.add(UnaryInstruction(target, "not", operand))
        return target
        
    def cmp_eq(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(MachineType.I1)
        self.current_block.add(CompareInstruction(target, "cmp_eq", left, right))
        return target
        
    def cmp_ne(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(MachineType.I1)
        self.current_block.add(CompareInstruction(target, "cmp_ne", left, right))
        return target
        
    def cmp_lt(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(MachineType.I1)
        self.current_block.add(CompareInstruction(target, "cmp_lt", left, right))
        return target
        
    def cmp_le(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(MachineType.I1)
        self.current_block.add(CompareInstruction(target, "cmp_le", left, right))
        return target
        
    def cmp_gt(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(MachineType.I1)
        self.current_block.add(CompareInstruction(target, "cmp_gt", left, right))
        return target
        
    def cmp_ge(self, left: VirtualRegister, right: VirtualRegister) -> VirtualRegister:
        target = self._next_vreg(MachineType.I1)
        self.current_block.add(CompareInstruction(target, "cmp_ge", left, right))
        return target
        
    def load(self, type: MachineType, ptr: VirtualRegister | StackSlot) -> VirtualRegister:
        target = self._next_vreg(type)
        self.current_block.add(LoadInstruction(target, ptr))
        return target
        
    def store(self, ptr: VirtualRegister | StackSlot, source: VirtualRegister):
        self.current_block.add(StoreInstruction(ptr, source))
        
    def set_arg(self, index: int, value: VirtualRegister):
        self.current_block.add(SetArgInstruction(index, value))
        
    def call(self, func_name: str, retval_type: MachineType | None) -> VirtualRegister | None:
        self.current_block.add(CallInstruction(func_name))
        if retval_type:
            target = self._next_vreg(retval_type)
            self.current_block.add(GetRetvalInstruction(target))
            return target
        return None
        
    def jmp(self, target_block: BlockID):
        self.current_block.add(JumpInstruction(target_block))
        
    def br(self, condition: VirtualRegister, true_block: BlockID, false_block: BlockID):
        self.current_block.add(BranchInstruction(condition, true_block, false_block))
        
    def ret(self, value: VirtualRegister | None = None):
        self.current_block.add(ReturnInstruction(value))
