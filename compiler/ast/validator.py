from .visitors import Visitor
from .base import Node
from .statements import *
from .declarations import *

class ASTValidatorError(Exception):
    def __init__(self, message, span):
        super().__init__(f"Validation Error at {span}: {message}")
        self.message = message
        self.span = span

class ASTValidator(Visitor):
    def __init__(self):
        self.in_loop = 0
        self.in_function = 0
        self.declared_classes = set()
        self.declared_interfaces = set()

    def validate(self, node: Node):
        self.visit(node)

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_FunctionDecl(self, node):
        self.in_function += 1
        param_names = set()
        for _, name in node.params:
            if name in param_names:
                raise ASTValidatorError(f"Duplicate parameter name '{name}'", node.span)
            param_names.add(name)
            
        for stmt in node.body:
            self.visit(stmt)
        self.in_function -= 1

    def visit_ClassDecl(self, node):
        if node.name in self.declared_classes:
            raise ASTValidatorError(f"Duplicate class name '{node.name}'", node.span)
        self.declared_classes.add(node.name)
        for stmt in node.body:
            self.visit(stmt)

    def visit_InterfaceDecl(self, node):
        if node.name in self.declared_interfaces:
            raise ASTValidatorError(f"Duplicate interface name '{node.name}'", node.span)
        self.declared_interfaces.add(node.name)
        for stmt in node.body:
            self.visit(stmt)

    def visit_LoopStatement(self, node):
        self.in_loop += 1
        for stmt in node.body:
            self.visit(stmt)
        self.in_loop -= 1

    def visit_WhileStatement(self, node):
        self.in_loop += 1
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)
        self.in_loop -= 1

    def visit_ForStatement(self, node):
        self.in_loop += 1
        self.visit(node.iterable)
        for stmt in node.body:
            self.visit(stmt)
        self.in_loop -= 1

    def visit_BreakStatement(self, node):
        if self.in_loop == 0:
            raise ASTValidatorError("'roko' (break) outside of loop", node.span)

    def visit_ContinueStatement(self, node):
        if self.in_loop == 0:
            raise ASTValidatorError("'agla' (continue) outside of loop", node.span)

    def visit_ReturnStatement(self, node):
        if self.in_function == 0:
            raise ASTValidatorError("'lautao' (return) outside of function", node.span)
        if node.expression:
            self.visit(node.expression)

    # For other nodes, simply traverse down
    def visit_IfStatement(self, node):
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)
        for cond, body in node.elifs:
            self.visit(cond)
            for stmt in body:
                self.visit(stmt)
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

    def visit_ExpressionStatement(self, node):
        self.visit(node.expression)

    def visit_AssignmentExpression(self, node):
        self.visit(node.target)
        self.visit(node.value)
        
    def visit_BinaryExpression(self, node):
        self.visit(node.left)
        self.visit(node.right)
        
    def visit_UnaryExpression(self, node):
        self.visit(node.operand)
        
    def visit_CallExpression(self, node):
        self.visit(node.callee)
        for arg in node.arguments:
            self.visit(arg)
            
    def visit_MemberExpression(self, node):
        self.visit(node.object_expr)
        
    def visit_IndexExpression(self, node):
        self.visit(node.object_expr)
        self.visit(node.index_expr)
        
    def visit_ResultUnwrapExpression(self, node):
        self.visit(node.operand)
        
    def visit_ListLiteral(self, node):
        for expr in node.elements:
            self.visit(expr)
            
    def visit_DictLiteral(self, node):
        for k, v in node.pairs:
            self.visit(k)
            self.visit(v)
            
    def visit_VariableDecl(self, node):
        if node.value:
            self.visit(node.value)
            
    def visit_ImportDecl(self, node):
        pass
        
    def visit_ExportDecl(self, node):
        self.visit(node.declaration)
        
    def visit_MatchStatement(self, node):
        pass
        
    def visit_NumberLiteral(self, node):
        pass
        
    def visit_StringLiteral(self, node):
        pass
        
    def visit_BoolLiteral(self, node):
        pass
        
    def visit_NullLiteral(self, node):
        pass
        
    def visit_IdentifierExpression(self, node):
        pass
