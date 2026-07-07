class IRBuilderPass:
    def __init__(self):
        self.context = None
        self.program = None
        self.temp_count = 0

    def new_temp(self):
        t = f"t{self.temp_count}"
        self.temp_count += 1
        return t

    def run(self, context):
        from compiler.ir.lir import ProgramIR, FunctionIR, BasicBlock, LIRInstruction, Operand
        from compiler.frontend.ast import ASTVisitor
        
        self.context = context
        self.program = ProgramIR()
        self.context.lir = self.program
        
        class Builder(ASTVisitor):
            def __init__(self, p):
                self.p = p
                self.current_func = None
                self.current_block = None
                
            def emit(self, opcode, *operands, dest=None):
                instr = LIRInstruction(opcode, list(operands), dest=dest)
                self.current_block.add(instr)
                return instr

            def visit_ProgramNode(self, node):
                # Separate functions and globals
                from compiler.frontend.ast import FunctionDeclNode
                functions = [s for s in node.statements if isinstance(s, FunctionDeclNode)]
                globals = [s for s in node.statements if not isinstance(s, FunctionDeclNode)]
                
                # Visit functions first
                for func in functions:
                    self.visit(func)
                
                # Main function (only if there are global statements)
                if globals:
                    self.current_func = FunctionIR("main")
                    self.p.program.functions.append(self.current_func)
                    self.current_block = self.current_func.new_block("entry")
                    
                    for stmt in globals:
                        self.visit(stmt)
                        
                    self.emit("RETURN")

            def visit_FunctionDeclNode(self, node):
                prev_func = self.current_func
                prev_block = self.current_block
                
                self.current_func = FunctionIR(node.identifier)
                self.p.program.functions.append(self.current_func)
                self.current_block = self.current_func.new_block("entry")
                
                # Parameters...
                for stmt in node.body:
                    self.visit(stmt)
                    
                self.emit("RETURN")
                
                self.current_func = prev_func
                self.current_block = prev_block

            def visit_VariableDeclNode(self, node):
                if node.expression:
                    val = self.visit(node.expression)
                    self.emit("STORE_VAR", Operand(val, is_var=True), Operand(node.identifier, is_var=True))
                else:
                    # Default init
                    pass

            def visit_AssignmentNode(self, node):
                val = self.visit(node.expression)
                self.emit("STORE_VAR", Operand(val, is_var=True), Operand(node.identifier, is_var=True))

            def visit_LiteralNode(self, node):
                t = self.p.new_temp()
                val = node.value
                if node.literal_type == "STRING":
                    val = f'"{val}"'
                self.emit("LOAD_CONST", Operand(val), dest=t)
                return t

            def visit_IdentifierNode(self, node):
                t = self.p.new_temp()
                self.emit("LOAD_VAR", Operand(node.name, is_var=True), dest=t)
                return t

            def visit_BinaryExpressionNode(self, node):
                left = self.visit(node.left)
                right = self.visit(node.right)
                t = self.p.new_temp()
                self.emit("BINARY_OP", Operand(node.operator), Operand(left, is_var=True), Operand(right, is_var=True), dest=t)
                return t

            def visit_IfNode(self, node):
                cond = self.visit(node.condition)
                
                then_b = self.current_func.new_block("if_then")
                end_b = self.current_func.new_block("if_end")
                
                self.emit("BRANCH", Operand(cond, is_var=True), Operand("if_then"), Operand("if_end"))
                
                self.current_block = then_b
                for stmt in node.body:
                    self.visit(stmt)
                self.emit("JUMP", Operand("if_end"))
                
                self.current_block = end_b

            def visit_WhileNode(self, node):
                cond_b = self.current_func.new_block("while_cond")
                body_b = self.current_func.new_block("while_body")
                end_b = self.current_func.new_block("while_end")
                
                self.emit("JUMP", Operand("while_cond"))
                
                self.current_block = cond_b
                cond = self.visit(node.condition)
                self.emit("BRANCH", Operand(cond, is_var=True), Operand("while_body"), Operand("while_end"))
                
                self.current_block = body_b
                for stmt in node.body:
                    self.visit(stmt)
                self.emit("JUMP", Operand("while_cond"))
                
                self.current_block = end_b

            def visit_ForNode(self, node):
                start = self.p.new_temp()
                self.emit("LOAD_CONST", Operand("0"), dest=start)
                self.emit("STORE_VAR", Operand(start, is_var=True), Operand(node.identifier, is_var=True))
                
                cond_b = self.current_func.new_block("for_cond")
                body_b = self.current_func.new_block("for_body")
                end_b = self.current_func.new_block("for_end")
                
                self.emit("JUMP", Operand("for_cond"))
                self.current_block = cond_b
                
                end_val = self.visit(node.range_expr)
                t_cond = self.p.new_temp()
                it = self.p.new_temp()
                self.emit("LOAD_VAR", Operand(node.identifier, is_var=True), dest=it)
                self.emit("BINARY_OP", Operand("<"), Operand(it, is_var=True), Operand(end_val, is_var=True), dest=t_cond)
                
                self.emit("BRANCH", Operand(t_cond, is_var=True), Operand("for_body"), Operand("for_end"))
                
                self.current_block = body_b
                for stmt in node.body:
                    self.visit(stmt)
                
                # Increment
                it2 = self.p.new_temp()
                one = self.p.new_temp()
                it3 = self.p.new_temp()
                self.emit("LOAD_VAR", Operand(node.identifier, is_var=True), dest=it2)
                self.emit("LOAD_CONST", Operand("1"), dest=one)
                self.emit("BINARY_OP", Operand("+"), Operand(it2, is_var=True), Operand(one, is_var=True), dest=it3)
                self.emit("STORE_VAR", Operand(it3, is_var=True), Operand(node.identifier, is_var=True))
                
                self.emit("JUMP", Operand("for_cond"))
                
                self.current_block = end_b

            def visit_FunctionCallStatementNode(self, node):
                self.visit(node.call_expr)

            def visit_FunctionCallNode(self, node):
                args = []
                for arg in node.args:
                    args.append(self.visit(arg))
                
                t = self.p.new_temp()
                ops = [Operand(node.identifier, is_var=True)] + [Operand(a, is_var=True) for a in args]
                self.emit("CALL", *ops, dest=t)
                return t
                
        if self.context.ast:
            Builder(self).visit(self.context.ast)
