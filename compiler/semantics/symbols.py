class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, type_name):
        self.symbols[name] = type_name

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

class SymbolResolutionPass:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.context = None

    def run(self, context):
        from compiler.frontend.ast import ASTVisitor
        self.context = context
        
        # Add Raylib globals
        self.global_scope.define("RAYWHITE", "Color")
        self.global_scope.define("RED", "Color")
        self.global_scope.define("DARKGRAY", "Color")
        self.global_scope.define("MAROON", "Color")
        self.global_scope.define("LIGHTGRAY", "Color")
        
        self.context.symbol_table = self.global_scope
        
        class Resolver(ASTVisitor):
            def __init__(self, pass_instance):
                self.p = pass_instance

            def visit_ProgramNode(self, node):
                for stmt in node.statements:
                    self.visit(stmt)

            def visit_FunctionDeclNode(self, node):
                # We do not strictly type functions in v0.4 yet, just note they exist
                self.p.current_scope.define(node.identifier, "function")
                
                # Enter new scope
                prev = self.p.current_scope
                self.p.current_scope = SymbolTable(parent=prev)
                
                for p_type, p_name in node.params:
                    self.p.current_scope.define(p_name, p_type)
                    
                for stmt in node.body:
                    self.visit(stmt)
                    
                # Restore scope
                self.p.current_scope = prev

            def visit_VariableDeclNode(self, node):
                if self.p.current_scope.lookup(node.identifier) and self.p.current_scope.parent is None:
                    # Basic check for globals
                    pass 
                self.p.current_scope.define(node.identifier, node.type_name)
                if node.expression:
                    self.visit(node.expression)

            def visit_AssignmentNode(self, node):
                if not self.p.current_scope.lookup(node.identifier):
                    self.p.context.diagnostics.error(
                        "L3001",
                        f"Variable '{node.identifier}' is not declared.",
                        0, 0, length=len(node.identifier) # TODO line/col in AST
                    )
                self.visit(node.expression)

            def visit_IdentifierNode(self, node):
                if not self.p.current_scope.lookup(node.name):
                    self.p.context.diagnostics.error(
                        "L3001",
                        f"Variable '{node.name}' is not declared.",
                        0, 0, length=len(node.name)
                    )

            def visit_IfNode(self, node):
                self.visit(node.condition)
                for stmt in node.body:
                    self.visit(stmt)

            def visit_WhileNode(self, node):
                self.visit(node.condition)
                for stmt in node.body:
                    self.visit(stmt)

            def visit_ForNode(self, node):
                self.visit(node.range_expr)
                
                prev = self.p.current_scope
                self.p.current_scope = SymbolTable(parent=prev)
                self.p.current_scope.define(node.identifier, "int")
                
                for stmt in node.body:
                    self.visit(stmt)
                    
                self.p.current_scope = prev

            def visit_FunctionCallStatementNode(self, node):
                self.visit(node.call_expr)

            def visit_FunctionCallNode(self, node):
                for arg in node.args:
                    self.visit(arg)

            def visit_BinaryExpressionNode(self, node):
                self.visit(node.left)
                self.visit(node.right)

        resolver = Resolver(self)
        if self.context.ast:
            resolver.visit(self.context.ast)
