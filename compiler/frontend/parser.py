from .lexer import TokenType, Token
from compiler.ast import *

class ParseError(Exception):
    def __init__(self, message, token):
        super().__init__(f"Parse Error at {token.line}:{token.column}: {message}")
        self.message = message
        self.token = token

class Parser:
    def __init__(self, tokens, file=""):
        self.tokens = tokens
        self.file = file
        self.pos = 0
        
    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return self.tokens[-1]
        
    def current(self):
        return self.peek(0)
        
    def match(self, *expected_types):
        if self.current().type in expected_types:
            return self.advance()
        return None
        
    def advance(self):
        token = self.current()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token
        
    def consume(self, expected_type, error_msg):
        token = self.match(expected_type)
        if not token:
            raise ParseError(error_msg, self.current())
        return token

    def _span(self, start_tok: Token, end_tok: Token) -> Span:
        return Span(self.file, start_tok.line, start_tok.column, end_tok.line, end_tok.column)

    def parse(self):
        statements = []
        while self.current().type != TokenType.EOF:
            if self.match(TokenType.NEWLINE):
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        # Whole program span
        if statements:
            span = Span(self.file, statements[0].span.start_line, statements[0].span.start_column, statements[-1].span.end_line, statements[-1].span.end_column)
        else:
            span = Span(self.file, 1, 1, 1, 1)
            
        return Program(span, statements)
        
    def parse_statement(self):
        token = self.current()
        
        if token.type == TokenType.KEYWORD:
            if token.value == "lala.laao":
                return self.parse_import()
            elif token.value == "lala.bahar":
                return self.parse_export()
            elif token.value == "lala.kaam":
                return self.parse_function_decl()
            elif token.value == "lala.varg":
                return self.parse_class_decl()
            elif token.value == "lala.swaroop":
                return self.parse_interface_decl()
            elif token.value == "lala.agar":
                return self.parse_if()
            elif token.value == "lala.jabtak":
                return self.parse_while()
            elif token.value == "lala.loop":
                return self.parse_loop()
            elif token.value == "lala.har":
                return self.parse_for()
            elif token.value == "lala.roko":
                return self.parse_break()
            elif token.value == "lala.agla":
                return self.parse_continue()
            elif token.value == "lala.lautao":
                return self.parse_return()
            elif token.value == "lala.match":
                return self.parse_match()
            elif token.value in ["lala.number", "lala.string", "lala.bool", "lala.list", "lala.dict"]:
                return self.parse_variable_decl(type_name=token.value)
                
        # Assignment or Expression Statement
        start_tok = self.current()
        expr = self.parse_expression()
        
        self.consume(TokenType.NEWLINE, "Expected newline after expression or assignment")
        
        return ExpressionStatement(self._span(start_tok, self.peek(-1)), expr)

    def parse_import(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_laao'")
        module_path = [self.consume(TokenType.IDENTIFIER, "Expected module name").value]
        while self.match(TokenType.DOT):
            module_path.append(self.consume(TokenType.IDENTIFIER, "Expected submodule name").value)
            
        alias = None
        if self.current().type == TokenType.KEYWORD and self.current().value == "as":
            self.advance()
            alias = self.consume(TokenType.IDENTIFIER, "Expected alias").value
            
        end_tok = self.consume(TokenType.NEWLINE, "Expected newline after import")
        return ImportDecl(self._span(tok, end_tok), ".".join(module_path), alias)

    def parse_export(self):
        # We don't support Export completely in Phase 7.2 AST yet, keeping simple.
        pass

    def parse_function_decl(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_kaam'")
        
        return_type = None
        if self.current().type == TokenType.KEYWORD and self.current().value in ["lala.number", "lala.string", "lala.bool", "lala.list", "lala.dict", "lala.result"]:
            return_type = self.advance().value
        elif self.current().type == TokenType.IDENTIFIER and self.peek(1).type != TokenType.LPAREN:
            return_type = self.advance().value
            
        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        self.consume(TokenType.LPAREN, "Expected '('")
        
        params = []
        if self.current().type != TokenType.RPAREN:
            while True:
                param_type = None
                if self.peek(1).type == TokenType.IDENTIFIER:
                    if self.current().type == TokenType.KEYWORD:
                        param_type = self.advance().value
                    elif self.current().type == TokenType.IDENTIFIER:
                        param_type = self.advance().value
                param_name = self.consume(TokenType.IDENTIFIER, "Expected parameter name").value
                params.append((param_type, param_name))
                if not self.match(TokenType.COMMA):
                    break
                    
        self.consume(TokenType.RPAREN, "Expected ')'")
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline before function body")
        
        body = self.parse_block()
        end_tok = self.peek(-1)
        return FunctionDecl(self._span(tok, end_tok), name, params, return_type, body)

    def parse_class_decl(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_varg'")
        name = self.consume(TokenType.IDENTIFIER, "Expected class name").value
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return ClassDecl(self._span(tok, self.peek(-1)), name, body)

    def parse_interface_decl(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_swaroop'")
        name = self.consume(TokenType.IDENTIFIER, "Expected interface name").value
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return InterfaceDecl(self._span(tok, self.peek(-1)), name, body)

    def parse_variable_decl(self, type_name):
        tok = self.advance() # consume type
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        
        expr = None
        if self.match(TokenType.ASSIGN):
            expr = self.parse_expression()
            
        end_tok = self.consume(TokenType.NEWLINE, "Expected newline")
        return VariableDecl(self._span(tok, end_tok), type_name, name, expr)

    def parse_if(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_agar'")
        condition = self.parse_expression()
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        
        elifs = []
        while self.current().type == TokenType.KEYWORD and self.current().value == "lala.warna_agar":
            self.advance()
            elif_cond = self.parse_expression()
            self.consume(TokenType.COLON, "Expected ':'")
            self.consume(TokenType.NEWLINE, "Expected newline")
            elif_body = self.parse_block()
            elifs.append((elif_cond, elif_body))
            
        else_body = None
        if self.current().type == TokenType.KEYWORD and self.current().value == "lala.warna":
            self.advance()
            self.consume(TokenType.COLON, "Expected ':'")
            self.consume(TokenType.NEWLINE, "Expected newline")
            else_body = self.parse_block()
            
        return IfStatement(self._span(tok, self.peek(-1)), condition, body, elifs, else_body)

    def parse_while(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_jabtak'")
        condition = self.parse_expression()
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return WhileStatement(self._span(tok, self.peek(-1)), condition, body)

    def parse_loop(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_loop'")
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return LoopStatement(self._span(tok, self.peek(-1)), body)

    def parse_for(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_har'")
        identifier = self.consume(TokenType.IDENTIFIER, "Expected identifier").value
        
        if self.current().type == TokenType.KEYWORD and self.current().value == "lala.in":
            self.advance()
            
        iterable = self.parse_expression()
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline")
        body = self.parse_block()
        return ForStatement(self._span(tok, self.peek(-1)), identifier, iterable, body)

    def parse_break(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_roko'")
        end_tok = self.consume(TokenType.NEWLINE, "Expected newline")
        return BreakStatement(self._span(tok, end_tok))

    def parse_continue(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_agla'")
        end_tok = self.consume(TokenType.NEWLINE, "Expected newline")
        return ContinueStatement(self._span(tok, end_tok))

    def parse_return(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_lautao'")
        expr = None
        if self.current().type != TokenType.NEWLINE:
            expr = self.parse_expression()
        end_tok = self.consume(TokenType.NEWLINE, "Expected newline")
        return ReturnStatement(self._span(tok, end_tok), expr)

    def parse_match(self):
        tok = self.consume(TokenType.KEYWORD, "Expected 'lala_match'")
        self.parse_expression() # Condition
        self.consume(TokenType.COLON, "Expected ':'")
        self.consume(TokenType.NEWLINE, "Expected newline")
        self.parse_block()
        return MatchStatement(self._span(tok, self.peek(-1)))

    def parse_block(self):
        self.consume(TokenType.INDENT, "Expected indentation")
        statements = []
        while self.current().type != TokenType.DEDENT and self.current().type != TokenType.EOF:
            if self.match(TokenType.NEWLINE):
                continue
            statements.append(self.parse_statement())
        self.consume(TokenType.DEDENT, "Expected dedent")
        return statements

    # Precedence: Assignment
    def parse_expression(self):
        start_tok = self.current()
        target = self.parse_logical_or()
        
        if self.match(TokenType.ASSIGN):
            value = self.parse_expression() # Right associative
            return AssignmentExpression(self._span(start_tok, self.peek(-1)), target, value)
            
        # Handle inferred variables if it's an Identifier on LHS of an implicit "="
        # But wait, "=" is AssignmentExpression now!
        # If target is IdentifierExpression and we just returned AssignmentExpression, that's exactly what an implicit variable decl or assignment is.
        # But wait, VariableDecl without keyword is just AssignmentExpression in AST. That is correct! 
        # The AST validator / Semantic analyzer will figure out if it's a declaration or assignment based on scope.
        
        return target

    # Precedence: or
    def parse_logical_or(self):
        start_tok = self.current()
        expr = self.parse_logical_and()
        while self.current().type == TokenType.KEYWORD and self.current().value == "or":
            self.advance()
            right = self.parse_logical_and()
            expr = BinaryExpression(self._span(start_tok, self.peek(-1)), expr, BinaryOperator.OR, right)
        return expr
        
    # Precedence: and
    def parse_logical_and(self):
        start_tok = self.current()
        expr = self.parse_equality()
        while self.current().type == TokenType.KEYWORD and self.current().value == "and":
            self.advance()
            right = self.parse_equality()
            expr = BinaryExpression(self._span(start_tok, self.peek(-1)), expr, BinaryOperator.AND, right)
        return expr

    # Precedence: == !=
    def parse_equality(self):
        start_tok = self.current()
        expr = self.parse_relational()
        while self.current().type in [TokenType.EQUAL, TokenType.NOT_EQUAL]:
            op = self.advance()
            op_enum = BinaryOperator.EQ if op.type == TokenType.EQUAL else BinaryOperator.NEQ
            right = self.parse_relational()
            expr = BinaryExpression(self._span(start_tok, self.peek(-1)), expr, op_enum, right)
        return expr

    # Precedence: < <= > >=
    def parse_relational(self):
        start_tok = self.current()
        expr = self.parse_additive()
        op_map = {
            TokenType.LESS: BinaryOperator.LT,
            TokenType.LESS_EQUAL: BinaryOperator.LTE,
            TokenType.GREATER: BinaryOperator.GT,
            TokenType.GREATER_EQUAL: BinaryOperator.GTE,
        }
        while self.current().type in op_map:
            op = self.advance()
            right = self.parse_additive()
            expr = BinaryExpression(self._span(start_tok, self.peek(-1)), expr, op_map[op.type], right)
        return expr

    # Precedence: + -
    def parse_additive(self):
        start_tok = self.current()
        expr = self.parse_multiplicative()
        op_map = {TokenType.PLUS: BinaryOperator.ADD, TokenType.MINUS: BinaryOperator.SUB}
        while self.current().type in op_map:
            op = self.advance()
            right = self.parse_multiplicative()
            expr = BinaryExpression(self._span(start_tok, self.peek(-1)), expr, op_map[op.type], right)
        return expr

    # Precedence: * / %
    def parse_multiplicative(self):
        start_tok = self.current()
        expr = self.parse_unary()
        op_map = {TokenType.STAR: BinaryOperator.MUL, TokenType.SLASH: BinaryOperator.DIV, TokenType.MODULO: BinaryOperator.MOD}
        while self.current().type in op_map:
            op = self.advance()
            right = self.parse_unary()
            expr = BinaryExpression(self._span(start_tok, self.peek(-1)), expr, op_map[op.type], right)
        return expr

    # Precedence: Unary - ! not
    def parse_unary(self):
        start_tok = self.current()
        if self.current().type == TokenType.MINUS:
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression(self._span(start_tok, self.peek(-1)), UnaryOperator.NEGATE, operand)
        elif self.current().type == TokenType.NOT or (self.current().type == TokenType.KEYWORD and self.current().value == "not"):
            self.advance()
            operand = self.parse_unary()
            return UnaryExpression(self._span(start_tok, self.peek(-1)), UnaryOperator.NOT, operand)
        return self.parse_postfix()

    # Precedence: () [] . ?
    def parse_postfix(self):
        start_tok = self.current()
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LPAREN): # Call
                args = []
                if self.current().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.parse_expression())
                self.consume(TokenType.RPAREN, "Expected ')'")
                expr = CallExpression(self._span(start_tok, self.peek(-1)), expr, args)
                
            elif self.match(TokenType.DOT): # Member Access
                prop = self.consume(TokenType.IDENTIFIER, "Expected property name")
                expr = MemberExpression(self._span(start_tok, self.peek(-1)), expr, prop.value)
                
            elif self.match(TokenType.LBRACKET): # Index Access
                index_expr = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']'")
                expr = IndexExpression(self._span(start_tok, self.peek(-1)), expr, index_expr)
                
            elif self.match(TokenType.QUESTION): # Result unwrap
                expr = ResultUnwrapExpression(self._span(start_tok, self.peek(-1)), expr)
                
            else:
                break
                
        return expr

    def parse_primary(self):
        tok = self.advance()
        span = self._span(tok, tok)
        
        if tok.type == TokenType.NUMBER_LITERAL:
            return NumberLiteral(span, tok.value)
        elif tok.type == TokenType.FLOAT_LITERAL:
            return NumberLiteral(span, tok.value)
        elif tok.type == TokenType.STRING_LITERAL:
            return StringLiteral(span, tok.value)
        elif tok.type == TokenType.BOOLEAN_LITERAL:
            return BoolLiteral(span, tok.value)
        elif tok.type == TokenType.IDENTIFIER:
            return IdentifierExpression(span, tok.value)
        elif tok.type == TokenType.LPAREN:
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')'")
            # Override span for parenthesized expr
            expr.span = self._span(tok, self.peek(-1))
            return expr
        elif tok.type == TokenType.LBRACKET: # List literal
            items = []
            if self.current().type != TokenType.RBRACKET:
                items.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    items.append(self.parse_expression())
            self.consume(TokenType.RBRACKET, "Expected ']'")
            return ListLiteral(self._span(tok, self.peek(-1)), items)
        elif tok.type == TokenType.LBRACE: # Dict literal
            pairs = []
            if self.current().type != TokenType.RBRACE:
                key = self.parse_expression()
                self.consume(TokenType.COLON, "Expected ':'")
                val = self.parse_expression()
                pairs.append((key, val))
                while self.match(TokenType.COMMA):
                    key = self.parse_expression()
                    self.consume(TokenType.COLON, "Expected ':'")
                    val = self.parse_expression()
                    pairs.append((key, val))
            self.consume(TokenType.RBRACE, "Expected '}'")
            return DictLiteral(self._span(tok, self.peek(-1)), pairs)
            
        raise ParseError(f"Unexpected token: {tok.type} ({tok.value})", tok)
