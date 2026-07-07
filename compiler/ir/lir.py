class Operand:
    def __init__(self, value, is_var=False):
        self.value = value
        self.is_var = is_var
        
    def __repr__(self):
        return str(self.value)

class LIRInstruction:
    def __init__(self, opcode, operands=None, dest=None):
        self.opcode = opcode
        self.operands = operands or []
        self.dest = dest

    def __repr__(self):
        ops = ", ".join(map(str, self.operands))
        if self.dest:
            return f"{self.dest} = {self.opcode} {ops}"
        return f"{self.opcode} {ops}"

class BasicBlock:
    def __init__(self, name):
        self.name = name
        self.instructions = []
        self.successors = [] # List of BasicBlock
        
    def add(self, instr):
        self.instructions.append(instr)
        
    def __repr__(self):
        lines = [f"{self.name}:"]
        for instr in self.instructions:
            lines.append(f"  {instr}")
        return "\n".join(lines)

class FunctionIR:
    def __init__(self, name):
        self.name = name
        self.blocks = []
        
    def new_block(self, name):
        block = BasicBlock(name)
        self.blocks.append(block)
        return block
        
    def __repr__(self):
        lines = [f"Function {self.name}:"]
        for b in self.blocks:
            lines.append(str(b))
        return "\n".join(lines)

class ProgramIR:
    def __init__(self):
        self.functions = []
        
    def __repr__(self):
        return "\n\n".join(map(str, self.functions))
