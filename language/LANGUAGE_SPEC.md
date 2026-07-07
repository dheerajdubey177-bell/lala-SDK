# Lala Language Specification v0.3

## 1. Overview
Lala is an explicitly indentation-sensitive, statically-typed programming language that uses Hinglish keywords. It compiles to C++ under the hood via the Lala SDK Compiler.

## 2. Lexical Structure

### 2.1 Indentation
Lala uses indentation to define block scope, similar to Python. 
- `INDENT` is generated when the indentation level increases.
- `DEDENT` is generated when the indentation level decreases.
- A block usually begins after a colon (`:`).

### 2.2 Keywords
All core control-flow keywords are prefixed with `lala.`.
- **Program Entry**: `lala.start:`
- **Conditionals**: `lala.agar`, `lala.warna_agar`, `lala.warna:`
- **Loops**: `lala.jab_tak`, `lala.har`
- **Functions**: `lala.kaam`, `lala.lautao`
- **I/O**: `lala.print`, `lala.pucho`
- **Types**: `lala.number` (int), `lala.decimal` (float), `lala.text` (string), `lala.flag` (bool)

### 2.3 Identifiers
Identifiers must start with a letter and can contain letters, numbers, and underscores.

### 2.4 Literals
- **Numbers**: Integers (e.g., `42`) and Floats (e.g., `3.14`).
- **Strings**: Enclosed in double quotes (`"Hello"`).
- **Booleans**: `true` or `false`.

## 3. Grammar (EBNF)

```ebnf
program        ::= "lala.start:" INDENT statement* DEDENT

statement      ::= var_decl 
                 | assignment 
                 | if_stmt 
                 | while_stmt 
                 | for_stmt
                 | func_decl 
                 | func_call 
                 | return_stmt 
                 | expr_stmt

var_decl       ::= type identifier "=" expression
type           ::= "lala.number" | "lala.decimal" | "lala.text" | "lala.flag"

assignment     ::= identifier "=" expression

if_stmt        ::= "lala.agar" expression ":" INDENT statement* DEDENT
                   ("lala.warna_agar" expression ":" INDENT statement* DEDENT)*
                   ("lala.warna:" INDENT statement* DEDENT)?

while_stmt     ::= "lala.jab_tak" expression ":" INDENT statement* DEDENT

for_stmt       ::= "lala.har" identifier "in" "range" "(" expression ")" ":" INDENT statement* DEDENT

func_decl      ::= "lala.kaam" type_or_void identifier "(" params? ")" ":" INDENT statement* DEDENT
type_or_void   ::= type | "void"
params         ::= type identifier ("," type identifier)*

return_stmt    ::= "lala.lautao" expression

func_call      ::= identifier "(" args? ")"
args           ::= expression ("," expression)*

expr_stmt      ::= expression

expression     ::= logical_or

logical_or     ::= logical_and ("or" logical_and)*
logical_and    ::= equality ("and" equality)*
equality       ::= comparison (("==" | "!=") comparison)*
comparison     ::= term ((">" | ">=" | "<" | "<=") term)*
term           ::= factor (("+" | "-") factor)*
factor         ::= primary (("*" | "/") primary)*

primary        ::= number | string | boolean | identifier | func_call | "(" expression ")"
```

## 4. Semantics & Scope
- **Static Typing**: Variables are statically typed and their type cannot change.
- **Lexical Scoping**: Variables declared in a block (`INDENT`) exist only within that block.
- **Global Scope**: Global variables are not supported in v0.3; all execution starts in `lala.start:`. Functions can be declared globally.

## 5. Standard API Namespaces
- `lala.graphics`
- `lala.input`
- `lala.math`
- `lala.collections`
