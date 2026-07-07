from .machine_ir import MachineFunction, MachineBlock, MachineInstruction, MachineOperand
from .machine_ir import Immediate, MemoryOperand, LabelOperand
from .registers import X86Register
from .opcodes import Opcode

class IntelAssemblyPrinter:
    def print_function(self, mfunc: MachineFunction) -> str:
        lines = []
        lines.append(".intel_syntax noprefix")
        lines.append(f".globl {mfunc.name}")
        lines.append(f"{mfunc.name}:")
        
        for block in mfunc.blocks:
            lines.append(f"{block.name}:")
            for instr in block.instructions:
                lines.append(f"    {self._print_instruction(instr)}")
                
        return "\n".join(lines)
        
    def _print_instruction(self, instr: MachineInstruction) -> str:
        opcode_str = instr.opcode.name.lower()
        if not instr.operands:
            return opcode_str
            
        ops = ", ".join(self._print_operand(op) for op in instr.operands)
        s = f"{opcode_str} {ops}"
        if instr.comment:
            s += f" # {instr.comment}"
        return s
        
    def _print_operand(self, op: MachineOperand) -> str:
        if isinstance(op, X86Register):
            return op.name
        elif isinstance(op, Immediate):
            return str(op.value)
        elif isinstance(op, MemoryOperand):
            # In intel syntax memory operands are [base + index*scale + disp]
            # Our Address str does exactly this:
            return f"QWORD PTR {op.address}"
        elif isinstance(op, LabelOperand):
            return op.name
        return str(op)
