from .core import *

class HIRPrinter:
    def format(self, program: Program) -> str:
        lines = []
        for func in program.functions:
            lines.append(f"Function {func.name}")
            for block in func.blocks:
                lines.append(f"  Block {block.id}")
                for instr in block.instructions:
                    lines.append(f"    {instr}")
            lines.append("")
        return "\n".join(lines)
