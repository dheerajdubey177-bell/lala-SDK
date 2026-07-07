# Lala Standard Library

Lala is a "batteries included" language. The standard library provides extensive functionality out of the box so beginners do not have to immediately learn package management.

## 1. Global Essentials

Only the absolute most fundamental capabilities are placed in the global namespace. This keeps the global namespace clean and prevents naming collisions.

The two global functions are:
- `print(value)`: Prints a value to the standard output.
- `input(prompt)`: Reads a line of text from the standard input.

```lala
name = input("What is your name?")
print("Hello, " + name)
```

## 2. Modules (Namespaces)

All other standard library functionality is organized into topical modules. Modules act as namespaces.

### Core Modules
- `math.*`: Mathematics (`sqrt()`, `random()`, `sin()`)
- `file.*`: File System (`open()`, `read()`, `write()`)
- `path.*`: File path manipulation
- `time.*`: Timers, delays, and dates
- `system.*`: OS-level operations (environment variables, exit)

### Media & Interaction
- `graphics.*`: 2D rendering (`window()`, `circle()`, `begin_drawing()`)
- `audio.*`: Sound playback
- `image.*`: Image loading and manipulation

### Network & Data
- `http.*`: Web requests (`get()`, `post()`)
- `json.*`: Data serialization
- `database.*`: SQLite database connections (`open()`, `execute()`)

### Intelligence
- `ai.*`: Native integrations with LLMs (`load()`, `chat()`)

## 3. Usage

To use a module, it must be explicitly imported using the `laao` keyword (see `modules.md`). 

```lala
laao graphics

graphics.window(800, 600)
graphics.circle(400, 300, 50)
```

By organizing standard functions under `graphics.*` or `file.*`, Lala guarantees that `file.open()` will never conflict with `database.open()`.
