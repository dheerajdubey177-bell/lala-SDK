from compiler.frontend.lexer import TokenType
import compiler.frontend.ast as ast

class Parser:
    def __init__(self, context):
        self.context = context
        self.tokens = context.tokens
        self.current = 0
        self.diagnostics = context.diagnostics

    def peek(self):
        if self.current >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.current]

    def advance(self):
        if self.current < len(self.tokens):
            self.current += 1
        return self.tokens[self.current - 1]

    def match(self, *types):
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, type_, error_msg):
        if self.peek().type == type_:
            return self.advance()
        token = self.peek()
        self.diagnostics.error(
            "L2001",
            f"Expected {type_.name}, got {token.value} ({token.type.name}): {error_msg}", 
            token.line, token.column, length=len(str(token.value))
        )
        # Simple error recovery: just return a dummy token and hope for the best
        return token

    def parse(self):
        statements = []
        while self.peek().type != TokenType.EOF:
            if self.peek().type == TokenType.NEWLINE:
                self.advance()
                continue
            
            token = self.peek()
            if token.type == TokenType.KEYWORD and token.value == "lala.start":
                self.advance()
                self.expect(TokenType.COLON, "Expected ':' after 'lala.start'")
                self.expect(TokenType.NEWLINE, "Expected newline")
                
                # Create a pseudo-function for lala.start
                body = self.parse_block()
                statements.append(ast.FunctionDeclNode("int", "main", [], body))
            else:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                    
        return ast.ProgramNode(statements)

    def parse_statement(self):
        token = self.peek()
        if token.type == TokenType.KEYWORD:
            if token.value in ["lala.number", "lala.decimal", "lala.text", "lala.flag"]:
                return self.parse_var_decl()
            elif token.value == "lala.agar":
                return self.parse_if()
            elif token.value == "lala.jab_tak":
                return self.parse_while()
            elif token.value == "lala.har":
                return self.parse_for()
            elif token.value == "lala.kaam":
                return self.parse_func_decl()
            elif token.value == "lala.lautao":
                return self.parse_return()
            elif token.value == "lala.khel_loop":
                return self.parse_khel_loop()
            elif token.value == "lala.khatam_drawing":
                self.advance()
                if self.peek().type == TokenType.LPAREN:
                    self.advance()
                    self.expect(TokenType.RPAREN, "Expected ')'")
                return ast.FunctionCallStatementNode(ast.FunctionCallNode("lala.khatam_drawing", []))
            elif token.value == "laao":
                return self.parse_import()
            elif token.value == "bahar":
                return self.parse_export()
            
        # Assignment, Function call, or custom type Variable declaration
        if token.type == TokenType.IDENTIFIER or (token.type == TokenType.KEYWORD and token.value.startswith("lala.")):
            # Special case for generic types like lala.collections.suchi<int>
            if token.value.startswith("lala.collections.suchi<"):
                return self.parse_var_decl()
            
            # Check if it's an assignment or a call
            # We look ahead
            if self.current + 1 < len(self.tokens):
                lookahead = self.tokens[self.current + 1]
                if lookahead.type == TokenType.ASSIGN:
                    return self.parse_assignment()
                elif lookahead.type == TokenType.LPAREN:
                    expr = self.parse_function_call()
                    return ast.FunctionCallStatementNode(expr)

        self.diagnostics.error("L2002", f"Unknown statement: {token.value}", token.line, token.column, length=len(str(token.value)))
        self.advance()
        return None

    def parse_import(self):
        self.advance() # laao
        id_token = self.expect(TokenType.IDENTIFIER, "Expected module path")
        module_path = id_token.value
        
        while self.peek().type == TokenType.DOT:
            self.advance()
            next_id = self.expect(TokenType.IDENTIFIER, "Expected submodule identifier")
            module_path += "." + next_id.value
            
        alias = None
        if self.peek().type == TokenType.KEYWORD and self.peek().value == "as":
            self.advance()
            alias_token = self.expect(TokenType.IDENTIFIER, "Expected alias identifier")
            alias = alias_token.value
            
        return ast.ImportNode(module_path, alias)

    def parse_export(self):
        self.advance() # bahar
        declaration = self.parse_statement()
        if not declaration:
            self.diagnostics.error("L2004", "Expected valid declaration after 'bahar'", self.peek().line, self.peek().column)
        return ast.ExportNode(declaration)

    def parse_var_decl(self):
        type_token = self.advance() # Consumes type
        id_token = self.expect(TokenType.IDENTIFIER, "Expected variable name")
        
        if self.match(TokenType.ASSIGN):
            expr = self.parse_expression()
        else:
            expr = None
            
        return ast.VariableDeclNode(type_token.value, id_token.value, expr)

    def parse_assignment(self):
        id_token = self.advance() # identifier
        self.expect(TokenType.ASSIGN, "Expected '='")
        expr = self.parse_expression()
        return ast.AssignmentNode(id_token.value, expr)

    def parse_if(self):
        self.advance() # lala.agar
        condition = self.parse_expression()
        self.expect(TokenType.COLON, "Expected ':'")
        self.expect(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        
        elifs = []
        else_body = []
        
        while self.peek().type == TokenType.KEYWORD and self.peek().value == "lala.warna_agar":
            self.advance()
            elif_cond = self.parse_expression()
            self.expect(TokenType.COLON, "Expected ':'")
            self.expect(TokenType.NEWLINE, "Expected newline")
            elif_body = self.parse_block()
            elifs.append((elif_cond, elif_body))
            
        if self.peek().type == TokenType.KEYWORD and self.peek().value == "lala.warna":
            self.advance()
            self.expect(TokenType.COLON, "Expected ':'")
            self.expect(TokenType.NEWLINE, "Expected newline")
            else_body = self.parse_block()
            
        return ast.IfNode(condition, body, elifs, else_body)

    def parse_while(self):
        self.advance()
        condition = self.parse_expression()
        self.expect(TokenType.COLON, "Expected ':'")
        self.expect(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return ast.WhileNode(condition, body)
        
    def parse_for(self):
        self.advance() # lala.har
        id_token = self.expect(TokenType.IDENTIFIER, "Expected loop variable")
        # Ensure 'in' and 'range' are matched. They are parsed as keywords
        in_token = self.expect(TokenType.KEYWORD, "Expected 'in'")
        range_token = self.expect(TokenType.KEYWORD, "Expected 'range'")
        self.expect(TokenType.LPAREN, "Expected '('")
        range_expr = self.parse_expression()
        self.expect(TokenType.RPAREN, "Expected ')'")
        self.expect(TokenType.COLON, "Expected ':'")
        self.expect(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return ast.ForNode(id_token.value, range_expr, body)

    def parse_khel_loop(self):
        self.advance()
        self.expect(TokenType.COLON, "Expected ':'")
        self.expect(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        cond = ast.FunctionCallNode("!WindowShouldClose", [])
        body.insert(0, ast.FunctionCallStatementNode(ast.FunctionCallNode("BeginDrawing", [])))
        return ast.WhileNode(cond, body)

    def parse_func_decl(self):
        self.advance() # lala.kaam
        type_token = self.advance() # return type
        id_token = self.expect(TokenType.IDENTIFIER, "Expected function name")
        self.expect(TokenType.LPAREN, "Expected '('")
        params = []
        if not self.match(TokenType.RPAREN):
            while True:
                p_type = self.advance()
                p_id = self.expect(TokenType.IDENTIFIER, "Expected parameter name")
                params.append((p_type.value, p_id.value))
                if not self.match(TokenType.COMMA):
                    break
            self.expect(TokenType.RPAREN, "Expected ')'")
            
        self.expect(TokenType.COLON, "Expected ':'")
        self.expect(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return ast.FunctionDeclNode(type_token.value, id_token.value, params, body)

    def parse_return(self):
        self.advance()
        expr = self.parse_expression()
        return ast.ReturnNode(expr)

    def parse_block(self):
        self.expect(TokenType.INDENT, "Expected indentation block")
        statements = []
        while self.peek().type != TokenType.DEDENT and self.peek().type != TokenType.EOF:
            if self.peek().type == TokenType.NEWLINE:
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.DEDENT, "Expected dedent")
        return statements

    def parse_expression(self):
        return self.parse_equality()

    def parse_equality(self):
        expr = self.parse_comparison()
        while self.peek().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance()
            right = self.parse_comparison()
            expr = ast.BinaryExpressionNode(expr, op.value, right)
        return expr

    def parse_comparison(self):
        expr = self.parse_term()
        while self.peek().type in (TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            op = self.advance()
            right = self.parse_term()
            expr = ast.BinaryExpressionNode(expr, op.value, right)
        return expr

    def parse_term(self):
        expr = self.parse_factor()
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance()
            right = self.parse_factor()
            expr = ast.BinaryExpressionNode(expr, op.value, right)
        return expr

    def parse_factor(self):
        expr = self.parse_primary()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            op = self.advance()
            right = self.parse_primary()
            expr = ast.BinaryExpressionNode(expr, op.value, right)
        return expr

    def parse_primary(self):
        token = self.advance()
        if token.type == TokenType.NUMBER:
            return ast.LiteralNode(token.value, "NUMBER")
        elif token.type == TokenType.FLOAT:
            return ast.LiteralNode(token.value, "FLOAT")
        elif token.type == TokenType.STRING:
            return ast.LiteralNode(token.value, "STRING")
        elif token.type == TokenType.BOOLEAN:
            return ast.LiteralNode(token.value, "BOOLEAN")
        elif token.type == TokenType.IDENTIFIER or (token.type == TokenType.KEYWORD and token.value.startswith("lala.")):
            # Could be identifier or function call
            if self.peek().type == TokenType.LPAREN:
                return self.parse_function_call(token.value)
            return ast.IdentifierNode(token.value)
        elif token.type == TokenType.LPAREN:
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')'")
            return expr
        elif token.type == TokenType.MINUS:
            # Unary minus
            expr = self.parse_primary()
            return ast.BinaryExpressionNode(ast.LiteralNode(0, "NUMBER"), "-", expr)
            
        self.diagnostics.error("L2002", f"Unexpected token in expression: {token.value}", token.line, token.column)
        return ast.LiteralNode(0, "NUMBER") # Recovery

    def parse_function_call(self, pre_parsed_id=None):
        if not pre_parsed_id:
            id_token = self.advance()
            pre_parsed_id = id_token.value
            
        self.expect(TokenType.LPAREN, "Expected '('")
        args = []
        if self.peek().type != TokenType.RPAREN:
            while True:
                args.append(self.parse_expression())
                if not self.match(TokenType.COMMA):
                    break
        self.expect(TokenType.RPAREN, "Expected ')'")
        return ast.FunctionCallNode(pre_parsed_id, args)
