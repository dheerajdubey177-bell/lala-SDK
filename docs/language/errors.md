# Lala Error Handling

Lala does not have Exceptions. There is no `try/catch/finally` syntax. Exceptions create hidden control flow that makes it difficult to trace where an error originated and where it is being handled. 

Instead, Lala uses **Result Types** and **Panics**.

## 1. The Result Type

Functions that can fail return a special built-in wrapper called a `result`. A `result` object contains either the successful value or an error message.

### Explicit Handling

You can explicitly check a result using the `.ok` property.

```lala
result file = file.open("data.txt")

agar file.ok:
    print(file.text)
warna:
    print("Error opening file: " + file.error)
```

## 2. The `?` Operator (Automatic Propagation)

If you do not want to handle the error immediately, you can append the `?` operator to a function call.

If the function succeeds, `?` unwraps the value. 
If the function fails, `?` immediately stops execution of the current function and returns the error to the caller.

```lala
kaam string read_config():
    // If open fails, read_config immediately returns the error
    file f = file.open("config.json") ?
    lautao f.text
```

This ensures that errors are never silently ignored, but keeps the code clean from endless `agar f.ok:` checks.

## 3. Panics

For truly unrecoverable errors (e.g., out of memory, or a missing graphics driver), use the `panic()` function. 

```lala
agar memory < 0:
    panic("System ran out of memory!")
```

A `panic` immediately crashes the program and prints a stack trace. It is not meant to be caught or recovered from. It should only be used when continuing execution would cause undefined behavior or data corruption.
