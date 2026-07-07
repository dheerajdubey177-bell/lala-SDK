from .base import Node, Span, NodeKind
from .expressions import Expression

class Statement(Node):
    pass

class IfStatement(Statement):
    def __init__(self, span: Span, condition: Expression, body: list[Statement], elifs: list[tuple[Expression, list[Statement]]], else_body: list[Statement] | None):
        super().__init__(span, NodeKind.IF_STATEMENT)
        self.condition = condition
        self.body = body
        self.elifs = elifs
        self.else_body = else_body

class WhileStatement(Statement):
    def __init__(self, span: Span, condition: Expression, body: list[Statement]):
        super().__init__(span, NodeKind.WHILE_STATEMENT)
        self.condition = condition
        self.body = body

class LoopStatement(Statement):
    def __init__(self, span: Span, body: list[Statement]):
        super().__init__(span, NodeKind.LOOP_STATEMENT)
        self.body = body

class ForStatement(Statement):
    def __init__(self, span: Span, identifier: str, iterable: Expression, body: list[Statement]):
        super().__init__(span, NodeKind.FOR_STATEMENT)
        self.identifier = identifier
        self.iterable = iterable
        self.body = body

class BreakStatement(Statement):
    def __init__(self, span: Span):
        super().__init__(span, NodeKind.BREAK_STATEMENT)

class ContinueStatement(Statement):
    def __init__(self, span: Span):
        super().__init__(span, NodeKind.CONTINUE_STATEMENT)

class ReturnStatement(Statement):
    def __init__(self, span: Span, expression: Expression | None):
        super().__init__(span, NodeKind.RETURN_STATEMENT)
        self.expression = expression

class ExpressionStatement(Statement):
    def __init__(self, span: Span, expression: Expression):
        super().__init__(span, NodeKind.EXPRESSION_STATEMENT)
        self.expression = expression

class MatchStatement(Statement):
    def __init__(self, span: Span):
        super().__init__(span, NodeKind.MATCH_STATEMENT)
        # Placeholder for future implementation
