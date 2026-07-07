from compiler.semantics.bound_ast import *
from .core import *

class HIRBuilder:
    def __init__(self, context):
        self.context = context
        self.next_val_id = 0
        self.next_block_id = 0
        
        self.current_function = None
        self.current_block = None
        
        # Maps VariableSymbol to the ValueID (pointer) returned by Allocate
        self.locals = {}

    def _next_val(self) -> ValueID:
        vid = ValueID(self.next_val_id)
        self.next_val_id += 1
        return vid
        
    def _next_block(self) -> BasicBlock:
        bid = BlockID(self.next_block_id)
        self.next_block_id += 1
        b = BasicBlock(bid)
        if self.current_function:
            self.current_function.add_block(b)
        return b

    def build(self, bound_program: BoundProgram) -> Program:
        prog = Program()
        for stmt in bound_program.statements:
            if isinstance(stmt, BoundFunctionDecl):
                self.next_val_id = 0
                self.next_block_id = 0
                self.locals = {}
                
                func = Function(stmt.symbol.name)
                prog.functions.append(func)
                self.current_function = func
                
                entry = self._next_block()
                self.current_block = entry
                
                for s in stmt.body:
                    self._build_stmt(s)
                    
                # Ensure last block has a terminator
                if self.current_block and not self.current_block.terminator:
                    self.current_block.add(Return(None))
                    
        return prog

    def _build_stmt(self, stmt: BoundStatement):
        if isinstance(stmt, BoundVariableDecl):
            # Allocate stack space
            ptr = self._next_val()
            # We assume symbols have types from context.type_registry, 
            # but since symbol itself doesn't explicitly store type in v1 (it's in node_types),
            # we can look up type from the declaration node or just assume dynamic.
            # Actually, `stmt.value.type` has the type.
            var_type = stmt.value.type if stmt.value else self.context.type_registry.UNKNOWN
            self.current_block.add(Allocate(ptr, var_type, stmt.symbol.name))
            self.locals[id(stmt.symbol)] = ptr
            
            if stmt.value:
                val = self._build_expr(stmt.value)
                self.current_block.add(Store(ptr, val))
                
        elif isinstance(stmt, BoundExpressionStatement):
            self._build_expr(stmt.expression)
            
        elif isinstance(stmt, BoundReturnStatement):
            val = self._build_expr(stmt.expression) if stmt.expression else None
            self.current_block.add(Return(val))
            # Any statements after return in the same BoundBlock are unreachable.
            # To handle this cleanly, we could create a dead block, but for now we just append.
            # (Dead code elimination pass can prune them).
            
        elif isinstance(stmt, BoundIfStatement):
            cond_val = self._build_expr(stmt.condition)
            
            true_block = self._next_block()
            false_block = self._next_block()
            merge_block = self._next_block()
            
            # Emit branch
            self.current_block.add(Branch(cond_val, true_block.id, false_block.id))
            
            # Build true path
            self.current_block = true_block
            for s in stmt.body.statements:
                self._build_stmt(s)
            if not self.current_block.terminator:
                self.current_block.add(Jump(merge_block.id))
                
            # Build false path
            self.current_block = false_block
            if stmt.else_body:
                for s in stmt.else_body.statements:
                    self._build_stmt(s)
            if not self.current_block.terminator:
                self.current_block.add(Jump(merge_block.id))
                
            self.current_block = merge_block

    def _build_expr(self, expr: BoundExpression) -> ValueID:
        if isinstance(expr, BoundLiteralExpression):
            val = self._next_val()
            self.current_block.add(Constant(val, expr.type, expr.value))
            return val
            
        elif isinstance(expr, BoundVariableExpression):
            ptr = self.locals[id(expr.symbol)]
            val = self._next_val()
            self.current_block.add(Load(val, expr.type, ptr))
            return val
            
        elif isinstance(expr, BoundAssignmentExpression):
            # Evaluate value
            val = self._build_expr(expr.value)
            
            if isinstance(expr.target, BoundVariableExpression):
                ptr = self.locals[id(expr.target.symbol)]
                self.current_block.add(Store(ptr, val))
                return val
            raise NotImplementedError("Only variable assignments are supported in HIR so far")
            
        elif isinstance(expr, BoundBinaryExpression):
            left = self._build_expr(expr.left)
            right = self._build_expr(expr.right)
            
            val = self._next_val()
            self.current_block.add(BinaryOp(val, expr.type, expr.operator.name, left, right))
            return val
            
        elif isinstance(expr, BoundIntrinsicCall):
            args = [self._build_expr(a) for a in expr.arguments]
            val = self._next_val() if expr.type != self.context.type_registry.VOID else None
            self.current_block.add(IntrinsicCall(val, expr.type, expr.intrinsic_id, args))
            return val
            
        elif isinstance(expr, BoundRuntimeCall):
            args = [self._build_expr(a) for a in expr.arguments]
            val = self._next_val() if expr.type != self.context.type_registry.VOID else None
            self.current_block.add(RuntimeCall(val, expr.type, expr.runtime_id, args, expr.side_effects, expr.pure))
            return val
            
        elif isinstance(expr, BoundFunctionCall):
            args = [self._build_expr(a) for a in expr.arguments]
            val = self._next_val() if expr.type != self.context.type_registry.VOID else None
            self.current_block.add(Call(val, expr.type, expr.symbol.name, args))
            return val

        raise NotImplementedError(f"Cannot lower expression {type(expr)}")
