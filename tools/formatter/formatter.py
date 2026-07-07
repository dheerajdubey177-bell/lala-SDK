from compiler.api import build_ast
from compiler.frontend.ast import *

class FormatterPass:
    """AST Unparser that enforces the canonical Lala style guide (4-space indents)."""
    
    def __init__(self):
        self.indent_level = 0
        self.output = []
        self.indent_str = "    " # 4 spaces
        
    def add_line(self, text):
        self.output.append((self.indent_str * self.indent_level) + text)
        
    def format(self, node):
        method_name = f"format_{type(node).__name__}"
        formatter = getattr(self, method_name, self.generic_format)
        return formatter(node)
        
    def generic_format(self, node):
        return f"/* UNSUPPORTED FORMAT NODE: {type(node).__name__} */"

    def format_ProgramNode(self, node):
        for stmt in node.statements:
            self.format(stmt)
        return "\n".join(self.output) + "\n"
        
    def format_ImportNode(self, node):
        line = f"laao {node.module_path}"
        if node.alias:
            line += f" as {node.alias}"
        self.add_line(line)
        
    def format_ExportNode(self, node):
        # Temp buffer
        old_output = self.output
        self.output = []
        self.format(node.declaration)
        decl_str = self.output[0]
        self.output = old_output
        
        self.add_line(f"bahar {decl_str.strip()}")
        
    def format_VariableDeclNode(self, node):
        line = f"{node.type_name} {node.identifier}"
        if node.expression:
            expr_str = self.format(node.expression)
            line += f" = {expr_str}"
        self.add_line(line)
        
    def format_AssignmentNode(self, node):
        expr_str = self.format(node.expression)
        self.add_line(f"{node.identifier} = {expr_str}")
        
    def format_FunctionCallStatementNode(self, node):
        self.add_line(self.format(node.call_expr))
        
    def format_ReturnNode(self, node):
        expr_str = self.format(node.expression)
        self.add_line(f"lala.lautao {expr_str}")
        
    def format_FunctionDeclNode(self, node):
        params_str = ", ".join([f"{ptype} {pname}" for ptype, pname in node.params])
        self.add_line(f"lala.kaam {node.return_type} {node.identifier}({params_str}):")
        self.indent_level += 1
        for stmt in node.body:
            self.format(stmt)
        self.indent_level -= 1
        self.add_line("") # Blank line after function

    def format_IfNode(self, node):
        cond_str = self.format(node.condition)
        self.add_line(f"lala.agar {cond_str}:")
        self.indent_level += 1
        for stmt in node.body:
            self.format(stmt)
        self.indent_level -= 1
        
        for e_cond, e_body in node.elifs:
            e_cond_str = self.format(e_cond)
            self.add_line(f"lala.warna_agar {e_cond_str}:")
            self.indent_level += 1
            for stmt in e_body:
                self.format(stmt)
            self.indent_level -= 1
            
        if node.else_body:
            self.add_line(f"lala.warna:")
            self.indent_level += 1
            for stmt in node.else_body:
                self.format(stmt)
            self.indent_level -= 1

    def format_WhileNode(self, node):
        if isinstance(node.condition, FunctionCallNode) and node.condition.identifier == "!WindowShouldClose":
            self.add_line(f"lala.khel_loop:")
            self.indent_level += 1
            for stmt in node.body:
                if isinstance(stmt, FunctionCallStatementNode) and stmt.call_expr.identifier == "BeginDrawing":
                    continue
                if isinstance(stmt, FunctionCallStatementNode) and stmt.call_expr.identifier == "lala.khatam_drawing":
                    continue
                self.format(stmt)
            self.add_line(f"lala.khatam_drawing()")
            self.indent_level -= 1
            return

        cond_str = self.format(node.condition)
        self.add_line(f"lala.jab_tak {cond_str}:")
        self.indent_level += 1
        for stmt in node.body:
            self.format(stmt)
        self.indent_level -= 1
        
    def format_ForNode(self, node):
        range_str = self.format(node.range_expr)
        self.add_line(f"lala.har {node.identifier} in range({range_str}):")
        self.indent_level += 1
        for stmt in node.body:
            self.format(stmt)
        self.indent_level -= 1

    # Expressions
    def format_BinaryExpressionNode(self, node):
        left = self.format(node.left)
        right = self.format(node.right)
        return f"{left} {node.operator} {right}"
        
    def format_FunctionCallNode(self, node):
        args_str = ", ".join([self.format(a) for a in node.args])
        return f"{node.identifier}({args_str})"
        
    def format_LiteralNode(self, node):
        if node.literal_type == "STRING":
            return f'"{node.value}"'
        elif node.literal_type == "BOOLEAN":
            return "true" if node.value else "false"
        return str(node.value)
        
    def format_IdentifierNode(self, node):
        return str(node.name)

def run_formatter(source_code):
    context = build_ast(source_code)
    if context.diagnostics.has_errors():
        # Cannot format invalid code safely
        return source_code
        
    formatter = FormatterPass()
    return formatter.format(context.ast)
