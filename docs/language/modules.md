# Lala Modules and Packages

Lala code is organized into modules. A module is simply a `.lala` file. 

## 1. Importing (`laao`)

The `laao` keyword brings another module into scope. 

```lala
laao math
laao graphics

graphics.window(800, 600)
number root = math.sqrt(16)
```

By default, everything in a module is kept private. 

## 2. Exporting (`bahar`)

To make a function, variable, or class accessible to files that import your module, use the `bahar` keyword.

**`src/physics.lala`**
```lala
bahar number gravity = 9.8

bahar kaam calculate_fall(number seconds):
    lautao gravity * seconds * seconds
```

**`src/main.lala`**
```lala
laao physics

print(physics.gravity)
```

## 3. Package Management (Future Syntax)

In v1.0, all `laao` statements refer to either the Standard Library or local files within the project. 

However, the syntax is intentionally reserved for future package management. In v2.0, `laao network_utils` could seamlessly download and import a community package without changing the language syntax.
