from .base import Node, Span, NodeKind

class LiteralExpression(Node):
    def __init__(self, span: Span, value):
        super().__init__(span, NodeKind.LITERAL_EXPRESSION)
        self.value = value

class NumberLiteral(LiteralExpression):
    pass

class StringLiteral(LiteralExpression):
    pass

class BoolLiteral(LiteralExpression):
    pass

class ListLiteral(LiteralExpression):
    def __init__(self, span: Span, elements):
        super().__init__(span, elements)
        self.elements = elements # List of expressions

class DictLiteral(LiteralExpression):
    def __init__(self, span: Span, pairs):
        super().__init__(span, pairs)
        self.pairs = pairs # List of tuples (key_expr, val_expr)

class NullLiteral(LiteralExpression):
    def __init__(self, span: Span):
        super().__init__(span, None)
