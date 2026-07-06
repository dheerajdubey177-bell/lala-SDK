# Lala SDK

Lala SDK is a powerful, highly optimized programming language and compiler that lets you write code in an intuitive, Python-like Hinglish syntax and instantly compiles it into native C++ Windows executables. It comes bundled with AAA game engine capabilities powered by Raylib!

## Features
- **Hinglish Pythonic Syntax**: No semicolons, no curly braces, fully indentation-based!
- **Native C++ Performance**: Translates directly to C++ source code before being natively compiled using GCC/MinGW.
- **AAA Game Engine Hooks**: Integrated directly with Raylib (5.0) to give you native windowing, 2D/3D graphics, and game loop management.
- **Zero-Dependency Execution**: Build `.exe` applications that run lightning fast on any Windows PC.

## Installation

1. Download the `Lala_SDK` zip package.
2. Extract it to a permanent folder on your computer (e.g., `C:\lala_sdk`).
3. Add the `bin/` directory to your Windows System `PATH` variable.
4. Open a command prompt and type `lala` to begin!

*(If you are building the SDK from source, run `build_sdk.bat` to generate the `lala.exe` compiler!)*

## Syntax Reference

Every keyword in the language starts with `lala.` for strict consistency.

### Variables & Data Types
```text
lala.number points = 100
lala.text name = "Developer"
lala.decimal speed = 4.5
lala.flag is_active = true
```

### Console I/O
```text
lala.print("Hello from Lala SDK!")
lala.pucho(name)
```

### Conditionals
```text
lala.agar points > 50:
    lala.print("You win!")
lala.warna_agar points == 50:
    lala.print("Tie!")
lala.warna:
    lala.print("Keep trying.")
```

### Loops
```text
lala.jab_tak points < 100:
    lala.print("Leveling up!")

lala.har i in range(10):
    lala.print(i)
```

## Raylib Game Development

Creating native games is ridiculously easy:

```text
lala.start:
    lala.banau_window(800, 600, "My Game Window")
    
    lala.khel_loop:
        lala.shuru_drawing()
        
        lala.draw_circle(400, 300, 50, BLUE)
        lala.draw_text("AAA graphics in Hinglish!", 190, 200, 20, LIGHTGRAY)
        
        lala.khatam_drawing()
```

### To compile your game:
```bash
lala my_game.lala
```
*(This automatically spits out `my_game.exe` which is ready to run!)*

## License

This project is open-source and licensed under the **Apache License 2.0**. See the `LICENSE` file for more details.
