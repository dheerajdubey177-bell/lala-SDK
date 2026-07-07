from compiler.ast.visitors import Visitor
from compiler.ast import *
from compiler.context import CompilationContext
from .symbols import VariableSymbol, FunctionSymbol
from .types import Type
from compiler.diagnostics.reporter import Diagnostic
from compiler.diagnostics.error_codes import ErrorCode, Severity

class TypeResolutionVisitor(Visitor):
    def __init__(self, context: CompilationContext):
        self.context = context

    def resolve(self, ast: Program):
        self.visit(ast)

    def _resolve_type_name(self, type_name: str | None, span: Span) -> Type | None:
        if not type_name:
            return None # Inferred type
            
        t = self.context.type_registry.get(type_name)
        if not t:
            # Here we might need to look up classes or interfaces
            # For v1.0, we just look up the global scope for ClassSymbol etc.
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.UNDEFINED_TYPE,
                severity=Severity.ERROR,
                span=span,
                message=f"Undefined type '{type_name}'."
            ))
            return self.context.type_registry.UNKNOWN
        return t

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VariableDecl(self, node: VariableDecl):
        if node.value:
            self.visit(node.value)
            
        resolved_type = self._resolve_type_name(node.type_name, node.span)
        if resolved_type:
            self.context.node_types[id(node)] = resolved_type
            
        sym = self.context.resolved_symbols.get(id(node))
        if sym and isinstance(sym, VariableSymbol):
            sym.resolved_type = resolved_type

    def visit_FunctionDecl(self, node: FunctionDecl):
        # Resolve return type
        ret_type = self._resolve_type_name(node.return_type, node.span) if node.return_type else self.context.type_registry.VOID
        self.context.node_types[id(node)] = ret_type
        
        sym = self.context.resolved_symbols.get(id(node))
        if sym and isinstance(sym, FunctionSymbol):
            sym.return_type = ret_type
        
        for param_type, param_name in node.params:
            if param_type:
                t = self._resolve_type_name(param_type, node.span)
                # To annotate the param symbol, we must look it up in the function scope
                if sym:
                    func_scope = self.context.node_scopes.get(id(node))
                    if func_scope:
                        param_sym = func_scope.resolve(param_name, current_only=True)
                        if param_sym and isinstance(param_sym, VariableSymbol):
                            param_sym.resolved_type = t
                
        for stmt in node.body:
            self.visit(stmt)

    # Pass through
    def visit_ClassDecl(self, node: ClassDecl):
        for stmt in node.body: self.visit(stmt)
    def visit_InterfaceDecl(self, node: InterfaceDecl):
        for stmt in node.body: self.visit(stmt)
    def visit_IfStatement(self, node: IfStatement):
        self.visit(node.condition)
        for stmt in node.body: self.visit(stmt)
        for cond, body in node.elifs:
            self.visit(cond)
            for stmt in body: self.visit(stmt)
        if node.else_body:
            for stmt in node.else_body: self.visit(stmt)
    def visit_WhileStatement(self, node: WhileStatement):
        self.visit(node.condition)
        for stmt in node.body: self.visit(stmt)
    def visit_LoopStatement(self, node: LoopStatement):
        for stmt in node.body: self.visit(stmt)
    def visit_ForStatement(self, node: ForStatement):
        self.visit(node.iterable)
        for stmt in node.body: self.visit(stmt)
    def visit_ExpressionStatement(self, node: ExpressionStatement):
        self.visit(node.expression)
    def visit_AssignmentExpression(self, node: AssignmentExpression):
        self.visit(node.target)
        self.visit(node.value)
    def visit_BinaryExpression(self, node: BinaryExpression):
        self.visit(node.left)
        self.visit(node.right)
    def visit_UnaryExpression(self, node: UnaryExpression):
        self.visit(node.operand)
    def visit_CallExpression(self, node: CallExpression):
        self.visit(node.callee)
        for arg in node.arguments: self.visit(arg)
    def visit_MemberExpression(self, node: MemberExpression):
        self.visit(node.object_expr)
    def visit_IndexExpression(self, node: IndexExpression):
        self.visit(node.object_expr)
        self.visit(node.index_expr)
    def visit_ResultUnwrapExpression(self, node: ResultUnwrapExpression):
        self.visit(node.operand)
    def visit_ListLiteral(self, node: ListLiteral):
        for expr in node.elements: self.visit(expr)
    def visit_DictLiteral(self, node: DictLiteral):
        for k, v in node.pairs:
            self.visit(k)
            self.visit(v)
    def visit_ReturnStatement(self, node: ReturnStatement):
        if node.expression: self.visit(node.expression)
    
    # Leaves
    def visit_IdentifierExpression(self, node): pass
    def visit_NumberLiteral(self, node): pass
    def visit_StringLiteral(self, node): pass
    def visit_BoolLiteral(self, node): pass
    def visit_NullLiteral(self, node): pass
    def visit_BreakStatement(self, node): pass
    def visit_ContinueStatement(self, node): pass
    def visit_ImportDecl(self, node): pass
    def visit_ExportDecl(self, node): pass
    def visit_MatchStatement(self, node): pass
