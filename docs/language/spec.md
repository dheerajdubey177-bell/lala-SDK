# Lala Language Specification (v1.0)

This document serves as the definitive source of truth for the Lala programming language. Backend implementations (C++, LLVM, JS) must adhere strictly to these semantics without exposing their internal constraints to the user.

---

## 1. Keywords & Primitives

Lala mixes English data types for international readability with Hindi keywords for cultural identity and control flow.

### Primitives
- `number`: A 64-bit floating point number (internally maps to `double` or `f64`).
- `string`: A UTF-8 text string.
- `bool`: A boolean value (`sach` or `jhooth`).
- `list`: A dynamic array.
- `dict`: A hash map.

### Keywords
- `kaam` (function definition)
- `agar` (if)
- `warna_agar` (else if)
- `warna` (else)
- `jabtak` (conditional while loop)
- `loop` (infinite loop)
- `har` (for loop)
- `roko` (break)
- `agla` (continue)
- `lautao` (return)
- `bahar` (export)
- `laao` (import)
- `varg` (class)
- `swaroop` (interface)

### Reserved Keywords (Future use)
- `async`, `await`, `match`, `enum`, `trait`

---

## 2. Variables & Constants

Variables are mutable by default.
```lala
number score = 0
string name = "Dheeraj"
list names = ["Ram", "Shyam", "Hari"]
```

---

## 3. Control Flow

### If / Else
No parentheses are required around conditions. Blocks are defined by colons and indentation.
```lala
agar score > 100:
    print("You win!")
warna_agar score > 50:
    print("Keep going!")
warna:
    print("Try again!")
```

### Loops
```lala
// For loop
har name in names:
    print(name)

// While loop
jabtak score < 100:
    score = score + 1
```

---

## 4. Functions

Defined using `kaam`. Types are optional but highly encouraged.

```lala
kaam number add(number a, number b):
    lautao a + b
```

---

## 5. Object Orientation (Composition over Inheritance)

Lala **does not support inheritance**. There is no `extends` or `super`. Lala relies on data Classes (`varg`), Interfaces (`swaroop`), and Composition.

### Classes (`varg`)
```lala
varg Player:
    string name
    number health

    kaam jump():
        print(name + " jumped!")
```

### Interfaces (`swaroop`)
Interfaces define behavior that classes can implement.
```lala
swaroop Drawable:
    kaam draw()
```

### Composition
Use composition to share functionality instead of inheritance trees.
```lala
varg Enemy:
    PlayerStats stats
    Weapon weapon
```

---

## 6. Error Handling

Lala uses **Result Types** instead of Exceptions. There is no `try/catch`. Hidden control flow is forbidden.

### The `?` Operator
Functions that can fail return a Result. The `?` operator unwraps the value if successful, or immediately returns the error up the call stack if it fails.

```lala
// If opening fails, the error is propagated automatically
file f = file.open("data.txt") ?
print(f.text)
```

### Explicit Checking
You can manually check if a result was successful using the `.ok` property.
```lala
result file = file.open("data.txt")

agar file.ok:
    print(file.text)
warna:
    print(file.error)
```

### Panics
For truly unrecoverable errors (e.g. out of memory, hardware failure), use `panic`. This immediately halts the program.
```lala
panic("Graphics device lost")
```

---

## 7. Memory Model

Lala manages memory silently. There are **no pointers**, no `new`, no `delete`, and no borrowing syntax.

```lala
class Node:
    number val

kaam create_node():
    Node n = Node()
    n.val = 5
    lautao n
```
*Implementation Note:* The backend is free to use Tracing Garbage Collection (like Java) or Automatic Reference Counting (like Swift/C++ `std::shared_ptr`) as long as the user never manually deallocates memory.

---

## 8. Batteries-Included Standard Library

Lala is batteries-included. Common capabilities like graphics, networking, databases, and AI are built into the global namespace. **No imports are required** for these core features.

### Graphics
```lala
window(800, 600, "My Game")
khel_loop:
    clear_background(0, 0, 0)
    circle(400, 300, 50, 255, 0, 0)
```

### AI
```lala
model = ai.load("llama")
string reply = model.ask("Hello world")
```

### HTTP
```lala
response = http.get("https://api.github.com")
print(response.body)
```

### Database
```lala
db = database.open("users.db")
db.execute("CREATE TABLE users (id, name)")
```
