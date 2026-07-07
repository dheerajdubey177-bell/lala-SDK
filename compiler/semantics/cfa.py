from .bound_ast import *
from .cfg import BasicBlock, ControlFlowGraph
from compiler.context import CompilationContext
from compiler.diagnostics.reporter import Diagnostic
from compiler.diagnostics.error_codes import ErrorCode, Severity

class CFGBuilder:
    def __init__(self, context: CompilationContext, name: str):
        self.context = context
        self.cfg = ControlFlowGraph(name)
        self.current_block = self.cfg.entry

    def build(self, statements: list[BoundStatement]) -> ControlFlowGraph:
        for stmt in statements:
            self._visit_statement(stmt)
            
        if self.current_block and self.current_block not in self.cfg.exit.predecessors:
            self.current_block.add_successor(self.cfg.exit)
            
        self._analyze_reachability()
        return self.cfg

    def _visit_statement(self, stmt: BoundStatement):
        if not self.current_block:
            # Unreachable code!
            self.context.diagnostics.report(Diagnostic(
                code=ErrorCode.UNREACHABLE_CODE,
                severity=Severity.WARNING,
                span=stmt.span,
                message="Unreachable code."
            ))
            return # Skip evaluating rest of unreachable statements in this sequence

        self.current_block.add_statement(stmt)

        if isinstance(stmt, BoundIfStatement):
            self._visit_if_statement(stmt)
        elif isinstance(stmt, BoundReturnStatement):
            self.current_block.add_successor(self.cfg.exit)
            self.current_block = None # Terminates current control flow

    def _visit_if_statement(self, stmt: BoundIfStatement):
        # We assume condition expression evaluation is already added to current block
        if_block = self.current_block
        
        true_block = self.cfg.create_block()
        if_block.add_successor(true_block)
        
        self.current_block = true_block
        for s in stmt.body.statements:
            self._visit_statement(s)
            
        true_exit = self.current_block
        
        false_exit = None
        if stmt.else_body:
            false_block = self.cfg.create_block()
            if_block.add_successor(false_block)
            
            self.current_block = false_block
            for s in stmt.else_body.statements:
                self._visit_statement(s)
            false_exit = self.current_block
        else:
            false_exit = if_block
            
        merge_block = self.cfg.create_block()
        if true_exit:
            true_exit.add_successor(merge_block)
        if false_exit:
            false_exit.add_successor(merge_block)
            
        self.current_block = merge_block

    def _analyze_reachability(self):
        # Determine if there are paths from Entry to Exit that don't pass through a return statement
        pass

class ControlFlowAnalyzer:
    def __init__(self, context: CompilationContext):
        self.context = context

    def analyze(self, ast: BoundProgram):
        for stmt in ast.statements:
            if isinstance(stmt, BoundFunctionDecl):
                builder = CFGBuilder(self.context, stmt.symbol.name)
                cfg = builder.build(stmt.body)
                
                # Check for missing returns if return type is not VOID
                if stmt.symbol.return_type != self.context.type_registry.VOID:
                    # If any predecessor of the exit block is NOT a return statement (i.e. it just fell through), error.
                    for pred in cfg.exit.predecessors:
                        if not pred.statements or not isinstance(pred.statements[-1], BoundReturnStatement):
                            self.context.diagnostics.report(Diagnostic(
                                code=ErrorCode.MISSING_RETURN,
                                severity=Severity.WARNING, # Warn for now
                                span=stmt.span,
                                message=f"Not all control paths in function '{stmt.symbol.name}' return a value."
                            ))
                            break
