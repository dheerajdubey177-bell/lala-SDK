# Lala Types & Variables

Lala is statically typed but supports heavy type inference to keep code looking clean.

## 1. Primitives

There are only three primitive data types:
- `number`: Represents both integers and floating-point values (internally a 64-bit float).
- `string`: Represents UTF-8 text.
- `bool`: Represents logical true/false (`true` or `false`).

## 2. Collections

There are two primary collections:
- `list`: A dynamically sized array of items.
- `dict`: A key-value hash map.

### Creating Collections
```lala
list names = ["Ram", "Shyam"]
dict scores = {"Ram": 100, "Shyam": 90}
```

## 3. Variables

Variables can be declared in two ways: explicit or inferred. There is no `let`, `var`, or `rakho` keyword. The first assignment is the declaration.

### Explicit Declarations
Use explicit declarations when you want to enforce a type upfront, or declare a variable without an immediate value.
```lala
number age = 20
string name = "Dheeraj"
```

### Inferred Declarations
The compiler will infer the type based on the right-hand side of the first assignment.
```lala
age = 20         // Inferred as number
name = "Dheeraj" // Inferred as string
```

## 4. Reassignment Rules

Variables are mutable. However, once a variable's type is established (explicitly or inferred), it **cannot** change.

```lala
age = 20
age = 30         // Allowed: number to number

age = "hello"    // Compilation Error: Cannot assign string to number
```
