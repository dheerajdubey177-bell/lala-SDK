from compiler.backend.base import Backend
from compiler.frontend.ast import *

class CppBackend(Backend):
    def __init__(self, context):
        super().__init__(context)
        self.headers = [
            '#include "lala_runtime.hpp"',
            '#include <iostream>',
            '#include <string>',
            '#include <vector>'
        ]
        self.indent_level = 0
        self.output_lines = []

    def add_line(self, line):
        self.output_lines.append(("    " * self.indent_level) + line)

    def generate_program(self):
        for h in self.headers:
            self.add_line(h)
        self.add_line("")
        
        self.visit(self.context.ast)
        
        return "\n".join(self.output_lines)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        self.add_line(f"// UNSUPPORTED NODE: {type(node).__name__}")
        return ""

    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_ImportNode(self, node):
        pass # Handle natively or via header injection
        
    def visit_ExportNode(self, node):
        self.visit(node.declaration)

    def visit_FunctionDeclNode(self, node):
        # map lala type to C++ type
        ret_type = "lala::number" if node.return_type == "lala.number" else "void"
        
        if node.identifier == "main":
            self.add_line("int main() {")
            self.indent_level += 1
            self.add_line("lala::init();")
        else:
            params = []
            for ptype, pname in node.params:
                cpp_type = "lala::number" if ptype == "lala.number" else "auto"
                params.append(f"{cpp_type} {pname}")
            
            self.add_line(f"{ret_type} {node.identifier}({', '.join(params)}) {{")
            self.indent_level += 1
            
        for stmt in node.body:
            self.visit(stmt)
            
        if node.identifier == "main":
            self.add_line("return 0;")
            
        self.indent_level -= 1
        self.add_line("}")
        self.add_line("")

    def visit_VariableDeclNode(self, node):
        cpp_type = "lala::number" if node.type_name == "lala.number" else "auto"
        if node.expression:
            expr_val = self.visit(node.expression)
            self.add_line(f"{cpp_type} {node.identifier} = {expr_val};")
        else:
            self.add_line(f"{cpp_type} {node.identifier};")
            
    def visit_AssignmentNode(self, node):
        expr_val = self.visit(node.expression)
        self.add_line(f"{node.identifier} = {expr_val};")

    def visit_FunctionCallStatementNode(self, node):
        expr_val = self.visit(node.call_expr)
        self.add_line(f"{expr_val};")

    def visit_ReturnNode(self, node):
        expr_val = self.visit(node.expression)
        self.add_line(f"return {expr_val};")

    def visit_IfNode(self, node):
        cond_val = self.visit(node.condition)
        self.add_line(f"if ({cond_val}) {{")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.add_line("}")
        
        for econd, ebody in node.elifs:
            econd_val = self.visit(econd)
            self.add_line(f"else if ({econd_val}) {{")
            self.indent_level += 1
            for stmt in ebody:
                self.visit(stmt)
            self.indent_level -= 1
            self.add_line("}")
            
        if node.else_body:
            self.add_line("else {")
            self.indent_level += 1
            for stmt in node.else_body:
                self.visit(stmt)
            self.indent_level -= 1
            self.add_line("}")

    def visit_WhileNode(self, node):
        is_game_loop = False
        if isinstance(node.condition, FunctionCallNode) and node.condition.identifier == "!WindowShouldClose":
            is_game_loop = True
            
        if is_game_loop:
            self.add_line("while (!lala::graphics::window_should_close()) {")
        else:
            cond_val = self.visit(node.condition)
            self.add_line(f"while ({cond_val}) {{")
            
        self.indent_level += 1
        
        for stmt in node.body:
            if isinstance(stmt, FunctionCallStatementNode) and stmt.call_expr.identifier == "BeginDrawing":
                self.add_line("lala::graphics::begin_drawing();")
                continue
            if isinstance(stmt, FunctionCallStatementNode) and stmt.call_expr.identifier == "lala.khatam_drawing":
                self.add_line("lala::graphics::end_drawing();")
                continue
                
            self.visit(stmt)
            
        self.indent_level -= 1
        self.add_line("}")

    def visit_FunctionCallNode(self, node):
        args = [self.visit(a) for a in node.args]
        args_str = ", ".join(args)
        
        func_name = node.identifier
        
        # Map builtins
        if func_name == "lala.print":
            return f"lala::print({args_str})"
        elif func_name == "lala.graphics.window":
            return f"lala::graphics::window({args_str})"
        elif func_name == "lala.graphics.clear_background":
            return f"lala::graphics::clear_background({args_str})"
        elif func_name == "lala.graphics.circle":
            return f"lala::graphics::circle({args_str})"
        elif func_name == "lala.graphics.begin_drawing":
            return f"lala::graphics::begin_drawing({args_str})"
        elif func_name == "lala.graphics.end_drawing":
            return f"lala::graphics::end_drawing({args_str})"
            
        elif func_name.startswith("lala."):
            cpp_func = func_name.replace(".", "::")
            return f"{cpp_func}({args_str})"
            
        return f"{func_name}({args_str})"

    def visit_BinaryExpressionNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.operator} {right})"
        
    def visit_LiteralNode(self, node):
        if node.literal_type == "STRING":
            return f'"{node.value}"'
        elif node.literal_type == "BOOLEAN":
            return "true" if node.value else "false"
        return str(node.value)
        
    def visit_IdentifierNode(self, node):
        return str(node.name)
