import os
import json
from compiler.ast.visitors import Visitor
from compiler.ast import *
from compiler.context import CompilationContext
from .symbols import *
from compiler.diagnostics.reporter import Diagnostic
from compiler.diagnostics.error_codes import ErrorCode, Severity

class NameResolutionVisitor(Visitor):
    def __init__(self, context: CompilationContext):
        self.context = context
        self.current_scope = context.global_scope

    def _push_scope(self, name: str) -> Scope:
        new_scope = Scope(parent=self.current_scope, name=name)
        self.current_scope = new_scope
        return new_scope

    def _pop_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent

    def resolve(self, ast: Program):
        # First, we define all built-ins in the global scope from intrinsics
        for builtin_fn in self.context.session.intrinsic_registry.intrinsics.keys():
            self.current_scope.define(FunctionSymbol(builtin_fn))
            
        self.visit(ast)

    def visit_Program(self, node: Program):
        self.context.node_scopes[id(node)] = self.current_scope
        for stmt in node.statements:
            self.visit(stmt)

    def visit_ImportDecl(self, node: ImportDecl):
        # Very simplified for now: just load the manifest if it matches runtime modules
        module_name = node.module_path.split('.')[0]
        alias_name = node.alias if node.alias else module_name
        
        manifest = self.context.session.get_runtime_manifest(module_name)
        if manifest:
            mod_sym = ModuleSymbol(alias_name)
            mod_sym.scope = Scope(parent=self.current_scope, name=f"Module_{alias_name}")
            
            for fn in manifest.get("functions", []):
                mod_sym.scope.define(FunctionSymbol(fn["name"]))
                
            if not self.current_scope.define(mod_sym):
                self.context.diagnostics.report(Diagnostic(
                    code=ErrorCode.DUPLICATE_DECLARATION,
                    severity=Severity.ERROR,
                    span=node.span,
                    message=f"Duplicate module or alias '{alias_name}'"
                ))
        else:
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.UNDEFINED_MODULE,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Cannot find module '{module_name}'"
            ))

    def visit_FunctionDecl(self, node: FunctionDecl):
        func_sym = FunctionSymbol(node.name)
        if not self.current_scope.define(func_sym):
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.DUPLICATE_DECLARATION,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Function '{node.name}' is already defined."
            ))
        self.context.resolved_symbols[id(node)] = func_sym
            
        scope = self._push_scope(f"Function_{node.name}")
        self.context.node_scopes[id(node)] = scope
        
        for param_type, param_name in node.params:
            param_sym = VariableSymbol(param_name, is_parameter=True)
            if not scope.define(param_sym):
                self.context.diagnostics.report(Diagnostic(
                    code=ErrorCode.DUPLICATE_DECLARATION,
                    severity=Severity.ERROR,
                    span=node.span, # Ideal: param span, but we don't have it yet
                    message=f"Duplicate parameter name '{param_name}'"
                ))
            # Parameters aren't currently distinct AST nodes, they are tuples (str, str)
            # We'd have to store them in a dict if we wanted to resolve their symbols by id(tuple) which is bad.
            # But the IdentifierExpression inside the body will resolve to param_sym anyway!
                
        for stmt in node.body:
            self.visit(stmt)
            
        self._pop_scope()

    def visit_ClassDecl(self, node: ClassDecl):
        class_sym = ClassSymbol(node.name)
        if not self.current_scope.define(class_sym):
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.DUPLICATE_DECLARATION,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Class '{node.name}' is already defined."
            ))
            
        scope = self._push_scope(f"Class_{node.name}")
        self.context.node_scopes[id(node)] = scope
        for stmt in node.body:
            self.visit(stmt)
        self._pop_scope()

    def visit_VariableDecl(self, node: VariableDecl):
        # We visit the RHS first, so that variable cannot be used in its own initialization
        if node.value:
            self.visit(node.value)
            
        var_sym = VariableSymbol(node.name)
        if not self.current_scope.define(var_sym):
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.DUPLICATE_DECLARATION,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Variable '{node.name}' is already defined in this scope."
            ))
        self.context.resolved_symbols[id(node)] = var_sym

    def visit_IdentifierExpression(self, node: IdentifierExpression):
        sym = self.current_scope.resolve(node.name)
        if not sym:
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.UNDEFINED_VARIABLE,
                severity=Severity.ERROR,
                span=node.span,
                message=f"Undefined variable or function '{node.name}'."
            ))
        else:
            self.context.resolved_symbols[id(node)] = sym

    def visit_MemberExpression(self, node: MemberExpression):
        # In name resolution, we can only confidently resolve module properties 
        # if the LHS is exactly a resolved ModuleSymbol.
        # General member access on objects requires Type Resolution.
        self.visit(node.object_expr)
        
        # If the object is an identifier that resolved to a ModuleSymbol, we can resolve the member.
        if isinstance(node.object_expr, IdentifierExpression):
            obj_sym = self.context.resolved_symbols.get(id(node.object_expr))
            if isinstance(obj_sym, ModuleSymbol):
                member_sym = obj_sym.scope.resolve(node.property_name, current_only=True)
                if not member_sym:
                    self.context.diagnostics.report(Diagnostic(
                        code=ErrorCode.UNDEFINED_FUNCTION, # or variable
                        severity=Severity.ERROR,
                        span=node.span,
                        message=f"Module '{obj_sym.name}' has no member '{node.property_name}'."
                    ))
                else:
                    self.context.resolved_symbols[id(node)] = member_sym

    # For scopes (loops, ifs)
    def visit_IfStatement(self, node: IfStatement):
        self.visit(node.condition)
        
        scope = self._push_scope("IfBody")
        self.context.node_scopes[id(node)] = scope
        for stmt in node.body:
            self.visit(stmt)
        self._pop_scope()
        
        for cond, body in node.elifs:
            self.visit(cond)
            scope = self._push_scope("ElseIfBody")
            for stmt in body:
                self.visit(stmt)
            self._pop_scope()
            
        if node.else_body:
            scope = self._push_scope("ElseBody")
            for stmt in node.else_body:
                self.visit(stmt)
            self._pop_scope()

    def visit_WhileStatement(self, node: WhileStatement):
        self.visit(node.condition)
        scope = self._push_scope("WhileBody")
        self.context.node_scopes[id(node)] = scope
        for stmt in node.body:
            self.visit(stmt)
        self._pop_scope()

    def visit_LoopStatement(self, node: LoopStatement):
        scope = self._push_scope("LoopBody")
        self.context.node_scopes[id(node)] = scope
        for stmt in node.body:
            self.visit(stmt)
        self._pop_scope()

    def visit_ForStatement(self, node: ForStatement):
        self.visit(node.iterable)
        scope = self._push_scope("ForBody")
        self.context.node_scopes[id(node)] = scope
        
        loop_var = VariableSymbol(node.identifier)
        scope.define(loop_var)
        
        for stmt in node.body:
            self.visit(stmt)
        self._pop_scope()

    # Pass-through for other nodes
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
        for arg in node.arguments:
            self.visit(arg)
    def visit_IndexExpression(self, node: IndexExpression):
        self.visit(node.object_expr)
        self.visit(node.index_expr)
    def visit_ResultUnwrapExpression(self, node: ResultUnwrapExpression):
        self.visit(node.operand)
    def visit_ListLiteral(self, node: ListLiteral):
        for expr in node.elements:
            self.visit(expr)
    def visit_DictLiteral(self, node: DictLiteral):
        for k, v in node.pairs:
            self.visit(k)
            self.visit(v)
    def visit_ReturnStatement(self, node: ReturnStatement):
        if node.expression:
            self.visit(node.expression)
    def visit_InterfaceDecl(self, node: InterfaceDecl):
        class_sym = ClassSymbol(node.name) # Using ClassSymbol for now
        self.current_scope.define(class_sym)
        scope = self._push_scope(f"Interface_{node.name}")
        for stmt in node.body:
            self.visit(stmt)
        self._pop_scope()

    def visit_NumberLiteral(self, node: NumberLiteral): pass
    def visit_StringLiteral(self, node: StringLiteral): pass
    def visit_BoolLiteral(self, node: BoolLiteral): pass
    def visit_NullLiteral(self, node: NullLiteral): pass
    def visit_BreakStatement(self, node: BreakStatement): pass
    def visit_ContinueStatement(self, node: ContinueStatement): pass
    def visit_MatchStatement(self, node: MatchStatement): pass
