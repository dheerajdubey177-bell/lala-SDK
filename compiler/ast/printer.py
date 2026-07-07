from .visitors import Visitor
from .base import Node

class ASTPrinter(Visitor):
    def __init__(self):
        self.indent = 0
        self.output = []

    def print(self, node: Node) -> str:
        self.output = []
        self.visit(node)
        return "\n".join(self.output)

    def _emit(self, text: str):
        self.output.append("    " * self.indent + text)

    def visit_Program(self, node):
        self._emit("Program")
        self.indent += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent -= 1

    def visit_ImportDecl(self, node):
        if node.alias:
            self._emit(f"Import({node.module_path} as {node.alias})")
        else:
            self._emit(f"Import({node.module_path})")

    def visit_ExportDecl(self, node):
        self._emit("Export")
        self.indent += 1
        self.visit(node.declaration)
        self.indent -= 1

    def visit_FunctionDecl(self, node):
        self._emit(f"Function({node.name})")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    def visit_ClassDecl(self, node):
        self._emit(f"Class({node.name})")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    def visit_InterfaceDecl(self, node):
        self._emit(f"Interface({node.name})")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    def visit_VariableDecl(self, node):
        self._emit("VariableDecl")
        self.indent += 1
        if node.type_name:
            self._emit(node.type_name)
        else:
            self._emit("inferred")
        self._emit(node.name)
        if node.value:
            self.visit(node.value)
        self.indent -= 1

    def visit_IfStatement(self, node):
        self._emit("If")
        self.indent += 1
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)
        for cond, body in node.elifs:
            self.indent -= 1
            self._emit("ElseIf")
            self.indent += 1
            self.visit(cond)
            for stmt in body:
                self.visit(stmt)
        if node.else_body:
            self.indent -= 1
            self._emit("Else")
            self.indent += 1
            for stmt in node.else_body:
                self.visit(stmt)
        self.indent -= 1

    def visit_WhileStatement(self, node):
        self._emit("While")
        self.indent += 1
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    def visit_LoopStatement(self, node):
        self._emit("Loop")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    def visit_ForStatement(self, node):
        self._emit(f"For({node.identifier})")
        self.indent += 1
        self.visit(node.iterable)
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    def visit_BreakStatement(self, node):
        self._emit("Break")

    def visit_ContinueStatement(self, node):
        self._emit("Continue")

    def visit_ReturnStatement(self, node):
        self._emit("Return")
        if node.expression:
            self.indent += 1
            self.visit(node.expression)
            self.indent -= 1

    def visit_ExpressionStatement(self, node):
        self.visit(node.expression)

    def visit_MatchStatement(self, node):
        self._emit("Match")

    def visit_BinaryExpression(self, node):
        self._emit("BinaryExpression")
        self.indent += 1
        self._emit(node.operator.name)
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1

    def visit_UnaryExpression(self, node):
        self._emit("UnaryExpression")
        self.indent += 1
        self._emit(node.operator.name)
        self.visit(node.operand)
        self.indent -= 1

    def visit_AssignmentExpression(self, node):
        self._emit("AssignmentExpression")
        self.indent += 1
        self.visit(node.target)
        self.visit(node.value)
        self.indent -= 1

    def visit_CallExpression(self, node):
        self._emit("CallExpression")
        self.indent += 1
        self.visit(node.callee)
        for arg in node.arguments:
            self.visit(arg)
        self.indent -= 1

    def visit_MemberExpression(self, node):
        self._emit("MemberExpression")
        self.indent += 1
        self.visit(node.object_expr)
        self._emit(node.property_name)
        self.indent -= 1

    def visit_IndexExpression(self, node):
        self._emit("IndexExpression")
        self.indent += 1
        self.visit(node.object_expr)
        self.visit(node.index_expr)
        self.indent -= 1

    def visit_IdentifierExpression(self, node):
        self._emit(f"Identifier({node.name})")

    def visit_ResultUnwrapExpression(self, node):
        self._emit("ResultUnwrapExpression")
        self.indent += 1
        self.visit(node.operand)
        self.indent -= 1

    def visit_NumberLiteral(self, node):
        self._emit(f"NumberLiteral({node.value})")

    def visit_StringLiteral(self, node):
        self._emit(f"StringLiteral({node.value})")

    def visit_BoolLiteral(self, node):
        self._emit(f"BoolLiteral({node.value})")

    def visit_ListLiteral(self, node):
        self._emit("ListLiteral")
        self.indent += 1
        for expr in node.elements:
            self.visit(expr)
        self.indent -= 1

    def visit_DictLiteral(self, node):
        self._emit("DictLiteral")
        self.indent += 1
        for k, v in node.pairs:
            self.visit(k)
            self.visit(v)
        self.indent -= 1

    def visit_NullLiteral(self, node):
        self._emit("NullLiteral")
