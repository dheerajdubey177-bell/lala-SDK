# AST Invariants

The Abstract Syntax Tree (AST) serves as the primary internal API of the Lala compiler. To ensure that downstream compilation stages (AST Validator, Semantic Analyzer, HIR Generator, Optimizer, Backend) can operate safely and efficiently without redundant checks, the Parser guarantees the following invariants:

## 1. Structural Completeness
- **Source Spans:** Every single AST node has a valid `Span`, which includes `file`, `start_line`, `start_column`, `end_line`, and `end_column`.
- **Enums:** Operators are never stored as raw strings (e.g., `"+"`, `"-"`). They are strictly stored using their corresponding Enums (`BinaryOperator.ADD`, `UnaryOperator.NEGATE`).
- **No Backend Assumptions:** The AST purely models the Lala language syntax. It contains absolutely no concept of raylib, C++, memory models, or pointers. A `MemberExpression` is strictly an object and a property.

## 2. Declarations
- **Functions:** Every `FunctionDecl` contains a valid body (a list of statements). 
- **Imports:** Every `ImportDecl` contains at least one valid module path string.
- **Classes/Interfaces:** Every `ClassDecl` and `InterfaceDecl` contains a valid body.

## 3. Statements
- **If Statements:** Every `IfStatement` has a non-null condition expression.
- **Loops:** Every `LoopStatement`, `WhileStatement`, and `ForStatement` has a valid body.

## 4. Expressions
- **Binary Expressions:** Every `BinaryExpression` has exactly two non-null operands (left and right).
- **Unary Expressions:** Every `UnaryExpression` has exactly one non-null operand.
- **Calls:** Every `CallExpression` has a valid callee expression.
- **Member Access:** Every `MemberExpression` has a valid object expression and a non-empty property name string.

By guaranteeing these invariants, the Lala compiler pipeline remains robust, predictable, and decoupled.
