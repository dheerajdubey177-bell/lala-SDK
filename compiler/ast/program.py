from .base import Node, Span, NodeKind

class Program(Node):
    def __init__(self, span: Span, statements):
        super().__init__(span, NodeKind.PROGRAM)
        self.statements = statements
