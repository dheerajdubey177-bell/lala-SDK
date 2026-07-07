import compiler.ast as ast

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def declare(self, name, type_name):
        self.symbols[name] = type_name

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class SemanticAnalyzer:
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        
        # Built-in namespaces mapping
        self.builtins = [
            "lala.print", "lala.pucho", 
            "lala.graphics.window", "lala.graphics.circle", "lala.graphics.rectangle", "lala.graphics.text", "lala.graphics.clear",
            "lala.input.button", "lala.input.button_pressed", "lala.input.mouse_x", "lala.input.mouse_y",
            "lala.math.random", "lala.math.abs", "lala.math.clamp", "lala.math.sqrt", "lala.math.sin", "lala.math.cos", "lala.math.pi",
            "lala.collections.suchi", "lala.collections.jodo", "lala.collections.hatao", "lala.collections.lambai", "lala.collections.saaf", "lala.collections.khali", "lala.collections.sort", "lala.collections.reverse",
            "std::to_string"
        ]

    def analyze(self, ast_node):
        if isinstance(ast_node, ast.ProgramNode):
            self.visit_ProgramNode(ast_node)
        return not self.diagnostics.has_errors()

    def enter_scope(self):
        self.current_scope = SymbolTable(parent=self.current_scope)

    def leave_scope(self):
        self.current_scope = self.current_scope.parent

    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass # Handle unvisited safely

    def visit_VariableDeclNode(self, node):
        if self.current_scope.lookup(node.identifier):
            self.diagnostics.error(f"Variable '{node.identifier}' is already declared in this scope.", 0, 0)
        else:
            self.current_scope.declare(node.identifier, node.type_name)
        
        if node.expression:
            self.visit(node.expression)

    def visit_AssignmentNode(self, node):
        if not self.current_scope.lookup(node.identifier):
            self.diagnostics.error(f"Variable '{node.identifier}' is not declared.", 0, 0)
        self.visit(node.expression)

    def visit_FunctionDeclNode(self, node):
        self.current_scope.declare(node.identifier, node.return_type)
        self.enter_scope()
        for param_type, param_name in node.params:
            self.current_scope.declare(param_name, param_type)
        for stmt in node.body:
            self.visit(stmt)
        self.leave_scope()

    def visit_IfNode(self, node):
        self.visit(node.condition)
        self.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.leave_scope()
        
        for condition, body in node.elifs:
            self.visit(condition)
            self.enter_scope()
            for stmt in body:
                self.visit(stmt)
            self.leave_scope()
            
        if node.else_body:
            self.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            self.leave_scope()

    def visit_WhileNode(self, node):
        self.visit(node.condition)
        self.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.leave_scope()

    def visit_ForNode(self, node):
        self.visit(node.range_expr)
        self.enter_scope()
        self.current_scope.declare(node.identifier, "lala.number")
        for stmt in node.body:
            self.visit(stmt)
        self.leave_scope()

    def visit_FunctionCallStatementNode(self, node):
        self.visit(node.call_expr)

    def visit_ReturnNode(self, node):
        self.visit(node.expression)

    def visit_FunctionCallNode(self, node):
        # We check builtins manually, or if it was declared
        is_builtin = False
        for b in self.builtins:
            if node.identifier.startswith(b):
                is_builtin = True
                
        if not is_builtin and not self.current_scope.lookup(node.identifier):
            # In a real compiler we track function signatures. For v0.3 we allow it if it might be valid C++ or undeclared warning
            pass
            
        for arg in node.args:
            self.visit(arg)

    def visit_BinaryExpressionNode(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_IdentifierNode(self, node):
        if not self.current_scope.lookup(node.name):
            # Warn that identifier isn't tracked. Might be a C++ native.
            pass
