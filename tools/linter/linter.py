from compiler.pass_manager import CompilerPass
from compiler.frontend.ast import ASTVisitor, VariableDeclNode, IdentifierNode, AssignmentNode
from compiler.api import build_ast

class UnusedVariablePass(CompilerPass, ASTVisitor):
    def run(self, context):
        self.context = context
        self.declared_vars = {} # identifier -> (node, line, col)
        self.used_vars = set()
        
        self.visit(context.ast)
        
        for var, (node, line, col) in self.declared_vars.items():
            if var not in self.used_vars:
                # Add a Warning diagnostic (W1001)
                context.diagnostics.error(
                    "W1001",
                    f"Unused variable '{var}'.",
                    line, col
                )
                
    def visit_VariableDeclNode(self, node):
        # We don't have token info in ASTNode right now natively, 
        # so we will use a dummy line/col or add it later.
        # For prototype, we'll just store the variable.
        self.declared_vars[node.identifier] = (node, 1, 1)
        if node.expression:
            self.visit(node.expression)
            
    def visit_IdentifierNode(self, node):
        self.used_vars.add(node.name)
        
    def visit_AssignmentNode(self, node):
        self.used_vars.add(node.identifier)
        self.visit(node.expression)
        
    def visit_ReturnNode(self, node):
        if node.expression:
            self.visit(node.expression)
            
    # Recurse into blocks
    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)
            
    def visit_FunctionDeclNode(self, node):
        for _, param_name in node.params:
            self.declared_vars[param_name] = (node, 1, 1)
        for stmt in node.body:
            self.visit(stmt)

class DeadCodePass(CompilerPass, ASTVisitor):
    def run(self, context):
        self.context = context
        self.visit(context.ast)
        
    def visit_FunctionDeclNode(self, node):
        has_returned = False
        for stmt in node.body:
            if has_returned:
                self.context.diagnostics.error("W1002", "Unreachable code detected after return statement.", 1, 1)
                break
            if type(stmt).__name__ == "ReturnNode":
                has_returned = True
                
    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

def run_linter(source_code, file_path="<memory>"):
    context = build_ast(source_code, file_path)
    
    if context.diagnostics.has_errors():
        # Syntax errors prevent linting
        return context.diagnostics
        
    # Run linter passes
    unused_pass = UnusedVariablePass()
    unused_pass.run(context)
    
    dead_code_pass = DeadCodePass()
    dead_code_pass.run(context)
    
    return context.diagnostics
