from .base import Node, Span, NodeKind, BinaryOperator, UnaryOperator

class Expression(Node):
    pass

class BinaryExpression(Expression):
    def __init__(self, span: Span, left: Expression, operator: BinaryOperator, right: Expression):
        super().__init__(span, NodeKind.BINARY_EXPRESSION)
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(Expression):
    def __init__(self, span: Span, operator: UnaryOperator, operand: Expression):
        super().__init__(span, NodeKind.UNARY_EXPRESSION)
        self.operator = operator
        self.operand = operand

class AssignmentExpression(Expression):
    def __init__(self, span: Span, target: Expression, value: Expression):
        super().__init__(span, NodeKind.ASSIGNMENT_EXPRESSION)
        self.target = target
        self.value = value

class CallExpression(Expression):
    def __init__(self, span: Span, callee: Expression, arguments: list[Expression]):
        super().__init__(span, NodeKind.CALL_EXPRESSION)
        self.callee = callee
        self.arguments = arguments

class MemberExpression(Expression):
    def __init__(self, span: Span, object_expr: Expression, property_name: str):
        super().__init__(span, NodeKind.MEMBER_EXPRESSION)
        self.object_expr = object_expr
        self.property_name = property_name

class IndexExpression(Expression):
    def __init__(self, span: Span, object_expr: Expression, index_expr: Expression):
        super().__init__(span, NodeKind.INDEX_EXPRESSION)
        self.object_expr = object_expr
        self.index_expr = index_expr

class IdentifierExpression(Expression):
    def __init__(self, span: Span, name: str):
        super().__init__(span, NodeKind.IDENTIFIER_EXPRESSION)
        self.name = name

class ResultUnwrapExpression(Expression):
    def __init__(self, span: Span, operand: Expression):
        super().__init__(span, NodeKind.RESULT_UNWRAP_EXPRESSION)
        self.operand = operand
