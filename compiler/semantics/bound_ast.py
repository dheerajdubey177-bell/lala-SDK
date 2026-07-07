from compiler.ast.base import Span
from .types import Type
from .intrinsics import IntrinsicID, RuntimeID

class BoundNode:
    def __init__(self, original_ast_node, span: Span):
        self.original_ast_node = original_ast_node
        self.span = span

class BoundStatement(BoundNode):
    pass

class BoundExpression(BoundNode):
    def __init__(self, original_ast_node, span: Span, type: Type):
        super().__init__(original_ast_node, span)
        self.type = type

class BoundDeclaration(BoundStatement):
    pass

class BoundProgram(BoundNode):
    def __init__(self, original_ast_node, span: Span, statements: list[BoundStatement]):
        super().__init__(original_ast_node, span)
        self.statements = statements

class BoundVariableDecl(BoundDeclaration):
    def __init__(self, original_ast_node, span: Span, symbol, value: BoundExpression | None):
        super().__init__(original_ast_node, span)
        self.symbol = symbol # VariableSymbol
        self.value = value

class BoundFunctionDecl(BoundDeclaration):
    def __init__(self, original_ast_node, span: Span, symbol, body: list[BoundStatement]):
        super().__init__(original_ast_node, span)
        self.symbol = symbol # FunctionSymbol
        self.body = body

class BoundBlock(BoundStatement):
    def __init__(self, original_ast_node, span: Span, statements: list[BoundStatement]):
        super().__init__(original_ast_node, span)
        self.statements = statements

class BoundIfStatement(BoundStatement):
    def __init__(self, original_ast_node, span: Span, condition: BoundExpression, body: BoundBlock, else_body: BoundBlock | None):
        super().__init__(original_ast_node, span)
        self.condition = condition
        self.body = body
        self.else_body = else_body

class BoundWhileStatement(BoundStatement):
    def __init__(self, original_ast_node, span: Span, condition: BoundExpression, body: BoundBlock):
        super().__init__(original_ast_node, span)
        self.condition = condition
        self.body = body
        
class BoundLoopStatement(BoundStatement):
    def __init__(self, original_ast_node, span: Span, body: BoundBlock):
        super().__init__(original_ast_node, span)
        self.body = body

class BoundExpressionStatement(BoundStatement):
    def __init__(self, original_ast_node, span: Span, expression: BoundExpression):
        super().__init__(original_ast_node, span)
        self.expression = expression

class BoundVariableExpression(BoundExpression):
    def __init__(self, original_ast_node, span: Span, type: Type, symbol):
        super().__init__(original_ast_node, span, type)
        self.symbol = symbol

class BoundLiteralExpression(BoundExpression):
    def __init__(self, original_ast_node, span: Span, type: Type, value):
        super().__init__(original_ast_node, span, type)
        self.value = value

class BoundAssignmentExpression(BoundExpression):
    def __init__(self, original_ast_node, span: Span, type: Type, target: BoundExpression, value: BoundExpression):
        super().__init__(original_ast_node, span, type)
        self.target = target
        self.value = value

class BoundBinaryExpression(BoundExpression):
    def __init__(self, original_ast_node, span: Span, type: Type, operator, left: BoundExpression, right: BoundExpression):
        super().__init__(original_ast_node, span, type)
        self.operator = operator
        self.left = left
        self.right = right

class BoundUnaryExpression(BoundExpression):
    def __init__(self, original_ast_node, span: Span, type: Type, operator, operand: BoundExpression):
        super().__init__(original_ast_node, span, type)
        self.operator = operator
        self.operand = operand

class BoundIntrinsicCall(BoundExpression):
    def __init__(self, original_ast_node, span: Span, type: Type, intrinsic_id: IntrinsicID, arguments: list[BoundExpression]):
        super().__init__(original_ast_node, span, type)
        self.intrinsic_id = intrinsic_id
        self.arguments = arguments

class BoundRuntimeCall(BoundExpression):
    def __init__(self, original_ast_node, span: Span, type: Type, runtime_id: RuntimeID, arguments: list[BoundExpression], side_effects: bool, pure: bool):
        super().__init__(original_ast_node, span, type)
        self.runtime_id = runtime_id
        self.arguments = arguments
        self.side_effects = side_effects
        self.pure = pure

class BoundReturnStatement(BoundStatement):
    def __init__(self, original_ast_node, span: Span, expression: BoundExpression | None):
        super().__init__(original_ast_node, span)
        self.expression = expression
class BoundFunctionCall(BoundExpression):
    def __init__(self, original_ast_node, span, type, symbol, arguments):
        super().__init__(original_ast_node, span, type)
        self.symbol = symbol
        self.arguments = arguments
