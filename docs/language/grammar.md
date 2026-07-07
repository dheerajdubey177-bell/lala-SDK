# Lala EBNF Grammar

This document provides the formal grammar for the Lala language. The parser MUST strictly implement this grammar.

```ebnf
Program ::= Statement*

Statement ::= FunctionDecl
            | ClassDecl
            | InterfaceDecl
            | ImportStmt
            | ExportStmt
            | BlockStmt
            | NEWLINE

BlockStmt ::= IfStmt
            | LoopStmt
            | WhileStmt
            | ForStmt
            | ReturnStmt
            | BreakStmt
            | ContinueStmt
            | ExprStmt
            | VarDecl

Block ::= INDENT Statement* DEDENT

# Declarations
FunctionDecl  ::= "kaam" Type? Identifier "(" Parameters? ")" ":" NEWLINE Block
ClassDecl     ::= "varg" Identifier ":" NEWLINE Block
InterfaceDecl ::= "swaroop" Identifier ":" NEWLINE Block

Parameters ::= Parameter ("," Parameter)*
Parameter  ::= Type Identifier

# Imports and Exports
ImportStmt ::= "laao" Identifier ("." Identifier)* NEWLINE
ExportStmt ::= "bahar" Identifier NEWLINE

# Variables
VarDecl ::= Type? Identifier "=" Expression NEWLINE

# Control Flow
IfStmt ::= "agar" Expression ":" NEWLINE Block
           ("warna_agar" Expression ":" NEWLINE Block)*
           ("warna" ":" NEWLINE Block)?

LoopStmt ::= "loop" ":" NEWLINE Block
WhileStmt ::= "jabtak" Expression ":" NEWLINE Block

ForStmt ::= "har" Identifier "in" Expression ":" NEWLINE Block

ReturnStmt   ::= "lautao" Expression? NEWLINE
BreakStmt    ::= "roko" NEWLINE
ContinueStmt ::= "agla" NEWLINE

# Expressions
ExprStmt ::= Expression NEWLINE

Expression ::= LogicalOrExpr

LogicalOrExpr  ::= LogicalAndExpr ("or" LogicalAndExpr)*
LogicalAndExpr ::= EqualityExpr ("and" EqualityExpr)*
EqualityExpr   ::= RelationalExpr (("==" | "!=") RelationalExpr)*
RelationalExpr ::= AdditiveExpr (("<" | "<=" | ">" | ">=") AdditiveExpr)*
AdditiveExpr   ::= MultiplicativeExpr (("+" | "-") MultiplicativeExpr)*
MultiplicativeExpr ::= UnaryExpr (("*" | "/") UnaryExpr)*

UnaryExpr ::= ("-" | "!") UnaryExpr
            | PostfixExpr

PostfixExpr ::= PrimaryExpr
              | PostfixExpr "(" Arguments? ")"
              | PostfixExpr "." Identifier
              | PostfixExpr "[" Expression "]"
              | PostfixExpr "?"

PrimaryExpr ::= NUMBER
              | STRING
              | BOOLEAN
              | Identifier
              | "(" Expression ")"
              | "[" Expressions? "]"
              | "{" KeyValuePairs? "}"

Arguments ::= Expression ("," Expression)*
Expressions ::= Expression ("," Expression)*
KeyValuePairs ::= Expression ":" Expression ("," Expression ":" Expression)*

# Terminals
Type ::= "number" | "string" | "bool" | "list" | "dict" | Identifier
NUMBER ::= [0-9]+ ("." [0-9]+)?
STRING ::= '"' [^"]* '"'
BOOLEAN ::= "true" | "false"
Identifier ::= [a-zA-Z_] [a-zA-Z0-9_]*
```
