from enum import Enum, auto

class Span:
    def __init__(self, file: str, start_line: int, start_column: int, end_line: int, end_column: int):
        self.file = file
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column

    def __repr__(self):
        return f"{self.file}:{self.start_line}:{self.start_column}-{self.end_line}:{self.end_column}"

class NodeKind(Enum):
    PROGRAM = auto()
    
    # Declarations
    FUNCTION_DECL = auto()
    CLASS_DECL = auto()
    INTERFACE_DECL = auto()
    IMPORT_DECL = auto()
    VARIABLE_DECL = auto()
    
    # Statements
    IF_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    LOOP_STATEMENT = auto()
    FOR_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    EXPRESSION_STATEMENT = auto()
    MATCH_STATEMENT = auto()
    
    # Expressions
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    MEMBER_EXPRESSION = auto()
    INDEX_EXPRESSION = auto()
    IDENTIFIER_EXPRESSION = auto()
    RESULT_UNWRAP_EXPRESSION = auto()
    LITERAL_EXPRESSION = auto()

class BinaryOperator(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()
    EQ = auto()
    NEQ = auto()
    AND = auto()
    OR = auto()

class UnaryOperator(Enum):
    NEGATE = auto()
    NOT = auto()

class Node:
    def __init__(self, span: Span, kind: NodeKind):
        self.span = span
        self.node_kind = kind
