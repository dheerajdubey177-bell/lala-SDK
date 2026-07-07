from .bound_ast import *

class BasicBlock:
    def __init__(self, id: int):
        self.id = id
        self.statements: list[BoundStatement] = []
        self.predecessors: list['BasicBlock'] = []
        self.successors: list['BasicBlock'] = []
        
    def add_statement(self, stmt: BoundStatement):
        self.statements.append(stmt)
        
    def add_successor(self, successor: 'BasicBlock'):
        if successor not in self.successors:
            self.successors.append(successor)
        if self not in successor.predecessors:
            successor.predecessors.append(self)

class ControlFlowGraph:
    def __init__(self, name: str):
        self.name = name
        self.entry = BasicBlock(0)
        self.exit = BasicBlock(1)
        self.blocks = [self.entry, self.exit]
        
    def create_block(self) -> BasicBlock:
        block = BasicBlock(len(self.blocks))
        self.blocks.append(block)
        return block
