class TypeCheckingPass:
    def run(self, context):
        from compiler.frontend.ast import ASTVisitor
        self.context = context
        
        class TypeChecker(ASTVisitor):
            def __init__(self, p):
                self.p = p

            def visit_ProgramNode(self, node):
                for stmt in node.statements:
                    self.visit(stmt)

            def visit_FunctionDeclNode(self, node):
                for stmt in node.body:
                    self.visit(stmt)

            def visit_VariableDeclNode(self, node):
                if node.expression:
                    self.visit(node.expression)

            def visit_AssignmentNode(self, node):
                self.visit(node.expression)

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
                for stmt in node.body:
                    self.visit(stmt)

            def visit_FunctionCallStatementNode(self, node):
                self.visit(node.call_expr)

            def visit_FunctionCallNode(self, node):
                for arg in node.args:
                    self.visit(arg)

            def visit_BinaryExpressionNode(self, node):
                self.visit(node.left)
                self.visit(node.right)

        if self.context.ast:
            TypeChecker(self).visit(self.context.ast)
