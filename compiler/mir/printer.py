from .core import *

class MIRPrinter:
    def __init__(self):
        self.lines = []
        self.indent_level = 0
        
    def _emit(self, text: str):
        self.lines.append("  " * self.indent_level + text)
        
    def format(self, program: Program) -> str:
        self.lines = []
        for func in program.functions:
            self._emit(f"Function {func.name}")
            self.indent_level += 1
            for block in func.blocks:
                self._emit(f"Block {block.id}")
                self.indent_level += 1
                for instr in block.instructions:
                    self._emit(str(instr))
                self.indent_level -= 1
            self.indent_level -= 1
        return "\n".join(self.lines)
