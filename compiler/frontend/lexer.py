import re
from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    KEYWORD = auto()
    
    # Literals and Identifiers
    IDENTIFIER = auto()
    NUMBER_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    
    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    QUESTION = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    MODULO = auto()
    
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    
    # Logical Operators
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Structure
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, Line {self.line}:{self.column})"

KEYWORDS = {
    # Types
    "lala.number", "lala.string", "lala.bool", "lala.list", "lala.dict",
    
    # Control Flow
    "lala.agar", "lala.warna_agar", "lala.warna",
    "lala.jabtak", "lala.loop", "lala.har", "lala.in",
    "lala.roko", "lala.agla", "lala.lautao",
    
    # Declaration
    "lala.kaam", "lala.varg", "lala.swaroop",
    
    # Modules
    "lala.laao", "lala.bahar",
    
    # Error Handling (handled natively or by Result)
    "lala.panic", "lala.result",
    
    # Logical Operators (if treated as keywords, though often they are operators)
    "lala.and", "lala.or", "lala.not",
    
    # Reserved (Future)
    "lala.async", "lala.await", "lala.match", "lala.enum", "lala.trait"
}

class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"Lexer Error at {line}:{column}: {message}")
        self.message = message
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        if not self.source.endswith('\n'):
            self.source += '\n'
            
        self.tokens = []
        self.current_line = 1
        self.indent_stack = [0]
        
    def tokenize(self):
        lines = self.source.split('\n')
        in_block_comment = False
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Handle block comments
            if in_block_comment:
                if '###' in line:
                    in_block_comment = False
                    # Check if there is anything after ###
                    idx = line.find('###')
                    line = line[idx+3:]
                    stripped = line.strip()
                    if not stripped:
                        continue
                else:
                    continue
            
            if '###' in line:
                # Start of block comment
                in_block_comment = True
                # Extract anything before ###
                idx = line.find('###')
                line = line[:idx]
                stripped = line.strip()
                if not stripped:
                    continue

            if not stripped or stripped.startswith("#"):
                continue
                
            # Strip inline comments
            if '#' in line:
                idx = line.find('#')
                line = line[:idx]
                stripped = line.strip()
                if not stripped:
                    continue

            # Handle indentation (only if line is not empty/comment)
            raw_line = line.rstrip('\r\n')
            indent_length = len(raw_line) - len(raw_line.lstrip())
            
            if indent_length > self.indent_stack[-1]:
                self.indent_stack.append(indent_length)
                self.tokens.append(Token(TokenType.INDENT, "", line_num, 1))
            else:
                while indent_length < self.indent_stack[-1]:
                    self.indent_stack.pop()
                    self.tokens.append(Token(TokenType.DEDENT, "", line_num, 1))
                    
            if indent_length != self.indent_stack[-1]:
                raise LexerError("Inconsistent indentation", line_num, indent_length + 1)
                
            # Tokenize line content
            self._tokenize_line(raw_line.strip(), line_num, indent_length + 1)
            
            self.tokens.append(Token(TokenType.NEWLINE, "\\n", line_num, len(raw_line) + 1))
            
        # Dedent at EOF
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, "", line_num, 1))
            
        self.tokens.append(Token(TokenType.EOF, "", line_num, 1))
        return self.tokens

    def _tokenize_line(self, line, line_num, start_col):
        token_specification = [
            ('FLOAT',       r'\d+\.\d+'),     # Float
            ('NUMBER',      r'\d+'),          # Integer
            ('STRING',      r'"[^"]*"'),      # String literal
            ('ID_OR_KEY',   r'lala\.[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*'), # Identifiers or keywords
            ('OP',          r'==|!=|<=|>=|<|>|\+|-|\*|/|%|=|!|\?'), # Operators
            ('PUNCT',       r'\(|\)|\[|\]|\{|\}|,|:|\.'),     # Punctuation
            ('SKIP',        r'[ \t]+'),       # Skip over spaces and tabs
            ('MISMATCH',    r'.'),            # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        
        for mo in re.finditer(tok_regex, line):
            kind = mo.lastgroup
            value = mo.group()
            column = start_col + mo.start()
            
            if kind == 'FLOAT':
                self.tokens.append(Token(TokenType.FLOAT_LITERAL, float(value), line_num, column))
            elif kind == 'NUMBER':
                self.tokens.append(Token(TokenType.NUMBER_LITERAL, int(value), line_num, column))
            elif kind == 'STRING':
                self.tokens.append(Token(TokenType.STRING_LITERAL, value[1:-1], line_num, column))
            elif kind == 'ID_OR_KEY':
                if value == "true" or value == "false":
                    self.tokens.append(Token(TokenType.BOOLEAN_LITERAL, value == "true", line_num, column))
                elif value in KEYWORDS:
                    self.tokens.append(Token(TokenType.KEYWORD, value, line_num, column))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, value, line_num, column))
            elif kind == 'OP':
                op_map = {
                    '=': TokenType.ASSIGN, '==': TokenType.EQUAL, '!=': TokenType.NOT_EQUAL,
                    '<': TokenType.LESS, '<=': TokenType.LESS_EQUAL, '>': TokenType.GREATER,
                    '>=': TokenType.GREATER_EQUAL, '+': TokenType.PLUS, '-': TokenType.MINUS,
                    '*': TokenType.STAR, '/': TokenType.SLASH, '%': TokenType.MODULO,
                    '?': TokenType.QUESTION
                }
                # Handle boolean logical operators parsed as ID_OR_KEY above
                if value in op_map:
                    self.tokens.append(Token(op_map[value], value, line_num, column))
                elif value == '!':
                    self.tokens.append(Token(TokenType.NOT, value, line_num, column))
            elif kind == 'PUNCT':
                punct_map = {
                    '(': TokenType.LPAREN, ')': TokenType.RPAREN, '{': TokenType.LBRACE,
                    '}': TokenType.RBRACE, '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                    ',': TokenType.COMMA, ':': TokenType.COLON, '.': TokenType.DOT
                }
                if value in punct_map:
                    self.tokens.append(Token(punct_map[value], value, line_num, column))
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise LexerError(f"Unexpected character '{value}'", line_num, column)
