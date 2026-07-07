from .opcodes import Opcode
from .machine_ir import MachineInstruction, MachineOperand, MachineBlock, LabelOperand
from typing import List

class MachineBuilder:
    def __init__(self, block: MachineBlock):
        self.block = block
        
    def emit(self, opcode: Opcode, *operands: MachineOperand) -> MachineInstruction:
        instr = MachineInstruction(opcode, list(operands))
        self.block.instructions.append(instr)
        return instr

    def mov(self, dst: MachineOperand, src: MachineOperand):
        return self.emit(Opcode.MOV, dst, src)

    def add(self, dst: MachineOperand, src: MachineOperand):
        return self.emit(Opcode.ADD, dst, src)
        
    def sub(self, dst: MachineOperand, src: MachineOperand):
        return self.emit(Opcode.SUB, dst, src)
        
    def imul(self, dst: MachineOperand, src: MachineOperand):
        return self.emit(Opcode.IMUL, dst, src)
        
    def cmp(self, left: MachineOperand, right: MachineOperand):
        return self.emit(Opcode.CMP, left, right)
        
    def jmp(self, label: str):
        return self.emit(Opcode.JMP, LabelOperand(label))
        
    def je(self, label: str):
        return self.emit(Opcode.JE, LabelOperand(label))
        
    def jne(self, label: str):
        return self.emit(Opcode.JNE, LabelOperand(label))
        
    def jl(self, label: str):
        return self.emit(Opcode.JL, LabelOperand(label))
        
    def jle(self, label: str):
        return self.emit(Opcode.JLE, LabelOperand(label))
        
    def jg(self, label: str):
        return self.emit(Opcode.JG, LabelOperand(label))
        
    def jge(self, label: str):
        return self.emit(Opcode.JGE, LabelOperand(label))
        
    def call(self, target: MachineOperand):
        return self.emit(Opcode.CALL, target)
        
    def ret(self):
        return self.emit(Opcode.RET)
        
    def push(self, src: MachineOperand):
        return self.emit(Opcode.PUSH, src)
        
    def pop(self, dst: MachineOperand):
        return self.emit(Opcode.POP, dst)
