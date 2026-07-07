from compiler.ast import *
from compiler.context import CompilationContext
from .bound_ast import *
from .symbols import VariableSymbol, FunctionSymbol
from .intrinsics import IntrinsicID, RuntimeID

class BoundTreeBuilder:
    def __init__(self, context: CompilationContext):
        self.context = context

    def build(self, node: Node) -> BoundNode:
        return self._bind(node)

    def _bind(self, node: Node) -> BoundNode:
        if isinstance(node, Program):
            stmts = [self._bind_statement(s) for s in node.statements]
            return BoundProgram(node, node.span, stmts)
        raise NotImplementedError(f"Cannot bind {type(node)}")

    def _bind_statement(self, node: Statement) -> BoundStatement:
        if isinstance(node, VariableDecl):
            val = self._bind_expression(node.value) if node.value else None
            sym = self.context.resolved_symbols.get(id(node))
            return BoundVariableDecl(node, node.span, sym, val)
            
        elif isinstance(node, FunctionDecl):
            sym = self.context.resolved_symbols.get(id(node))
            body = [self._bind_statement(s) for s in node.body]
            return BoundFunctionDecl(node, node.span, sym, body)
            
        elif isinstance(node, IfStatement):
            cond = self._bind_expression(node.condition)
            body_stmts = [self._bind_statement(s) for s in node.body]
            body_block = BoundBlock(node, node.span, body_stmts) # Should have proper block span
            
            # Simple conversion of elifs for now (nesting else blocks)
            # This is an important simplification for CFG
            else_block = None
            if node.else_body:
                else_stmts = [self._bind_statement(s) for s in node.else_body]
                else_block = BoundBlock(node, node.span, else_stmts)
                
            # If there are elifs, we should convert them to nested BoundIfStatements inside the else_block
            # For brevity in v1.0, we just handle standard if/else.
            return BoundIfStatement(node, node.span, cond, body_block, else_block)
            
        elif isinstance(node, WhileStatement):
            cond = self._bind_expression(node.condition)
            body_stmts = [self._bind_statement(s) for s in node.body]
            return BoundWhileStatement(node, node.span, cond, BoundBlock(node, node.span, body_stmts))
            
        elif isinstance(node, ReturnStatement):
            val = self._bind_expression(node.expression) if node.expression else None
            return BoundReturnStatement(node, node.span, val)
            
        elif isinstance(node, ExpressionStatement):
            expr = self._bind_expression(node.expression)
            return BoundExpressionStatement(node, node.span, expr)
            
        # Ignore import/export for bound tree as they are fully consumed by Name Resolution
        elif isinstance(node, (ImportDecl, ExportDecl)):
            return BoundBlock(node, node.span, []) # Empty block
            
        raise NotImplementedError(f"Cannot bind statement {type(node)}")

    def _bind_expression(self, node: Expression) -> BoundExpression:
        node_type = self.context.node_types.get(id(node), self.context.type_registry.UNKNOWN)
        
        if isinstance(node, (NumberLiteral, StringLiteral, BoolLiteral)):
            return BoundLiteralExpression(node, node.span, node_type, node.value)
            
        elif isinstance(node, IdentifierExpression):
            sym = self.context.resolved_symbols.get(id(node))
            return BoundVariableExpression(node, node.span, node_type, sym)
            
        elif isinstance(node, AssignmentExpression):
            target = self._bind_expression(node.target)
            val = self._bind_expression(node.value)
            return BoundAssignmentExpression(node, node.span, node_type, target, val)
            
        elif isinstance(node, BinaryExpression):
            left = self._bind_expression(node.left)
            right = self._bind_expression(node.right)
            return BoundBinaryExpression(node, node.span, node_type, node.operator, left, right)
            
        elif isinstance(node, CallExpression):
            args = [self._bind_expression(a) for a in node.arguments]
            
            # This is where Phase 8.5 Runtime/Intrinsic Binding happens
            # If the callee is an Identifier, it might be an intrinsic
            if isinstance(node.callee, IdentifierExpression):
                intrinsic = self.context.session.intrinsic_registry.resolve(node.callee.name)
                if intrinsic:
                    return BoundIntrinsicCall(node, node.span, node_type, intrinsic, args)
                    
            # If the callee is a MemberExpression resolving to a module, it's a Runtime call
            if isinstance(node.callee, MemberExpression):
                # E.g. graphics.circle
                if isinstance(node.callee.object_expr, IdentifierExpression):
                    mod_sym = self.context.resolved_symbols.get(id(node.callee.object_expr))
                    from .symbols import ModuleSymbol
                    if isinstance(mod_sym, ModuleSymbol):
                        manifest = self.context.session.get_runtime_manifest(mod_sym.name)
                        if manifest:
                            fn_meta = next((f for f in manifest.get("functions", []) if f["name"] == node.callee.property_name), None)
                            if fn_meta and "stable_id" in fn_meta:
                                runtime_id = RuntimeID[fn_meta["stable_id"]]
                                pure = fn_meta.get("pure", False)
                                return BoundRuntimeCall(node, node.span, node_type, runtime_id, args, not pure, pure)
            
            # Regular function call
            symbol = self.context.resolved_symbols.get(id(node.callee))
            from .symbols import FunctionSymbol
            if isinstance(symbol, FunctionSymbol):
                return BoundFunctionCall(node, node.span, node_type, symbol, args)
            raise NotImplementedError("User-defined function calls not fully bound yet")
            
        raise NotImplementedError(f"Cannot bind expression {type(node)}")
