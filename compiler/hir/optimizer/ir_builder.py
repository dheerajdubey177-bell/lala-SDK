from compiler.hir.core import *

class IRBuilder:
    def __init__(self, original_program: Program):
        self.original = original_program
        self.new_program = Program()
        self.changed = False
        
        # State during rebuild
        self.current_function = None
        self.current_block = None
        
    def start_function(self, name: str):
        self.current_function = Function(name)
        self.new_program.functions.append(self.current_function)
        
    def start_block(self, block_id: BlockID):
        self.current_block = BasicBlock(block_id)
        if self.current_function:
            self.current_function.add_block(self.current_block)
            
    def add_instruction(self, instr: Instruction):
        self.current_block.add(instr)
        
    def reuse_block(self, block: BasicBlock):
        if self.current_function:
            self.current_function.add_block(block)
            
    def mark_changed(self):
        self.changed = True
