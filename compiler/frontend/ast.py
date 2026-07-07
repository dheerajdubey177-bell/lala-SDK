class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class StatementNode(ASTNode):
    pass

class ExpressionNode(ASTNode):
    pass

class ImportNode(StatementNode):
    def __init__(self, module_path, alias=None):
        self.module_path = module_path
        self.alias = alias

class ExportNode(StatementNode):
    def __init__(self, declaration):
        self.declaration = declaration
class VariableDeclNode(StatementNode):
    def __init__(self, type_name, identifier, expression):
        self.type_name = type_name
        self.identifier = identifier
        self.expression = expression

class AssignmentNode(StatementNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class FunctionDeclNode(StatementNode):
    def __init__(self, return_type, identifier, params, body):
        self.return_type = return_type
        self.identifier = identifier
        self.params = params
        self.body = body

class IfNode(StatementNode):
    def __init__(self, condition, body, elifs, else_body):
        self.condition = condition
        self.body = body
        self.elifs = elifs
        self.else_body = else_body

class WhileNode(StatementNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForNode(StatementNode):
    def __init__(self, identifier, range_expr, body):
        self.identifier = identifier
        self.range_expr = range_expr
        self.body = body

class FunctionCallStatementNode(StatementNode):
    def __init__(self, call_expr):
        self.call_expr = call_expr

class ReturnNode(StatementNode):
    def __init__(self, expression):
        self.expression = expression

class FunctionCallNode(ExpressionNode):
    def __init__(self, identifier, args):
        self.identifier = identifier
        self.args = args

class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class LiteralNode(ExpressionNode):
    def __init__(self, value, literal_type):
        self.value = value
        self.literal_type = literal_type # e.g. NUMBER, STRING, BOOLEAN

class IdentifierNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

class ASTVisitor:
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass
