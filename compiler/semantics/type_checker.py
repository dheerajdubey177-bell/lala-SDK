from compiler.ast.visitors import Visitor
from compiler.ast import *
from compiler.context import CompilationContext
from .symbols import VariableSymbol, FunctionSymbol
from .types import Type
from .type_system import TypeSystem
from compiler.diagnostics.reporter import Diagnostic
from compiler.diagnostics.error_codes import ErrorCode, Severity

class TypeCheckingVisitor(Visitor):
    def __init__(self, context: CompilationContext):
        self.context = context
        self.type_system = TypeSystem(context.type_registry)

    def check(self, ast: Program):
        self.visit(ast)

    def _type_of(self, node: Node) -> Type:
        t = self.context.node_types.get(id(node))
        return t if t else self.context.type_registry.UNKNOWN

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_NumberLiteral(self, node: NumberLiteral):
        self.context.node_types[id(node)] = self.context.type_registry.NUMBER
        
    def visit_StringLiteral(self, node: StringLiteral):
        self.context.node_types[id(node)] = self.context.type_registry.STRING
        
    def visit_BoolLiteral(self, node: BoolLiteral):
        self.context.node_types[id(node)] = self.context.type_registry.BOOL

    def visit_IdentifierExpression(self, node: IdentifierExpression):
        sym = self.context.resolved_symbols.get(id(node))
        if sym:
            # We assume VariableSymbol has a type assigned during declarations or previous inferences
            # For this simple v1.0, we just fetch it if it's there
            if isinstance(sym, VariableSymbol) and hasattr(sym, 'resolved_type') and sym.resolved_type:
                self.context.node_types[id(node)] = sym.resolved_type
            else:
                self.context.node_types[id(node)] = self.context.type_registry.UNKNOWN

    def visit_BinaryExpression(self, node: BinaryExpression):
        self.visit(node.left)
        self.visit(node.right)
        
        l_type = self._type_of(node.left)
        r_type = self._type_of(node.right)
        
        res_type = self.type_system.binary_result(node.operator, l_type, r_type)
        if not res_type:
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.TYPE_MISMATCH,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Operator '{node.operator.name}' is undefined for types '{l_type.name}' and '{r_type.name}'."
            ))
            self.context.node_types[id(node)] = self.context.type_registry.UNKNOWN
        else:
            self.context.node_types[id(node)] = res_type

    def visit_UnaryExpression(self, node: UnaryExpression):
        self.visit(node.operand)
        op_type = self._type_of(node.operand)
        
        res_type = self.type_system.unary_result(node.operator, op_type)
        if not res_type:
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.TYPE_MISMATCH,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Operator '{node.operator.name}' is undefined for type '{op_type.name}'."
            ))
            self.context.node_types[id(node)] = self.context.type_registry.UNKNOWN
        else:
            self.context.node_types[id(node)] = res_type

    def visit_AssignmentExpression(self, node: AssignmentExpression):
        self.visit(node.target)
        self.visit(node.value)
        
        t_type = self._type_of(node.target)
        v_type = self._type_of(node.value)
        
        if not self.type_system.is_assignable(t_type, v_type):
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.TYPE_MISMATCH,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Cannot assign '{v_type.name}' to '{t_type.name}'."
            ))
        
        self.context.node_types[id(node)] = v_type # Assignment yields value type

    def visit_VariableDecl(self, node: VariableDecl):
        if node.value:
            self.visit(node.value)
            
        declared_type = self.context.node_types.get(id(node))
        inferred_type = self._type_of(node.value) if node.value else None
        
        final_type = declared_type
        
        if declared_type and inferred_type:
            if not self.type_system.is_assignable(declared_type, inferred_type):
                self.context.diagnostics.report(Diagnostic(
                    code=ErrorCode.TYPE_MISMATCH,
                    severity=Severity.ERROR,
                    span=node.span,
                    message=f"Cannot initialize variable of type '{declared_type.name}' with value of type '{inferred_type.name}'."
                ))
        elif not declared_type and inferred_type:
            final_type = inferred_type
            
        if not final_type:
            final_type = self.context.type_registry.UNKNOWN
            
        # Push to symbol table
        sym = self.context.node_scopes.get(id(node))
        # wait, we didn't store scope for VariableDecl in 8.1.
        # But we can find the symbol from the parent scope or we should just let AST node hold it.

    def visit_IfStatement(self, node: IfStatement):
        self.visit(node.condition)
        cond_type = self._type_of(node.condition)
        if cond_type != self.context.type_registry.BOOL and cond_type != self.context.type_registry.UNKNOWN:
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.TYPE_MISMATCH,
                severity=Severity.ERROR,
                span=node.condition.span,
                message=f"Condition must be bool, found '{cond_type.name}'."
            ))
            
        for stmt in node.body: self.visit(stmt)
        for cond, body in node.elifs:
            self.visit(cond)
            # Check cond type
            for stmt in body: self.visit(stmt)
        if node.else_body:
            for stmt in node.else_body: self.visit(stmt)

    def visit_WhileStatement(self, node: WhileStatement):
        self.visit(node.condition)
        cond_type = self._type_of(node.condition)
        if cond_type != self.context.type_registry.BOOL and cond_type != self.context.type_registry.UNKNOWN:
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.TYPE_MISMATCH,
                severity=Severity.ERROR,
                span=node.condition.span,
                message=f"Condition must be bool, found '{cond_type.name}'."
            ))
        for stmt in node.body: self.visit(stmt)

    # Pass through
    def visit_ExpressionStatement(self, node: ExpressionStatement):
        self.visit(node.expression)
    def visit_FunctionDecl(self, node: FunctionDecl):
        for stmt in node.body: self.visit(stmt)
    def visit_ClassDecl(self, node: ClassDecl):
        for stmt in node.body: self.visit(stmt)
    def visit_LoopStatement(self, node: LoopStatement):
        for stmt in node.body: self.visit(stmt)
    def visit_ReturnStatement(self, node: ReturnStatement):
        if node.expression: self.visit(node.expression)
    def visit_CallExpression(self, node: CallExpression):
        self.visit(node.callee)
        for arg in node.arguments: self.visit(arg)
        # Simplified: set unknown for now
        self.context.node_types[id(node)] = self.context.type_registry.UNKNOWN
    def visit_MemberExpression(self, node: MemberExpression):
        self.visit(node.object_expr)
        self.context.node_types[id(node)] = self.context.type_registry.UNKNOWN
