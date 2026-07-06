# Lala SDK Setup Instructions

Welcome to the Lala SDK, the easiest and most powerful way to build software and games using an intuitive Hinglish syntax powered by a blazing-fast C++ engine!

## Packaging for Distribution

To distribute this SDK so anyone can use it, follow these steps:

1. Compile the Python engine into a standalone executable using PyInstaller:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile bin/lala_compiler.py
   ```
2. Move the generated `lala.exe` from the `dist/` folder into your `bin/` directory.
3. Download a portable MinGW/GCC release (e.g., w64devkit) and extract it. Copy `g++.exe` and its required DLLs into the `bin/` directory alongside `lala.exe`.
4. Zip the entire `lala_sdk` folder (including `bin`, `core`, and `templates`).
5. Share the Zip file with your users!

## Installation for End Users

When someone downloads your `lala_sdk.zip`, they simply need to:

1. Extract the folder to a permanent location, for example, `C:\lala_sdk`.
2. Add the compiler to their Windows PATH environment variable:
   - Open Windows Search and type "Environment Variables".
   - Click "Edit the system environment variables".
   - Under "System Variables", find the `Path` variable and click "Edit".
   - Click "New" and add the exact path to the `bin` directory (e.g., `C:\lala_sdk\bin`).
   - Click "OK" on all windows to save the changes.
3. Open a new Command Prompt or PowerShell window and type `lala` to verify it works!

## Your First Program

Create a file named `game.lala` anywhere on your computer:
```text
lala.start
    lala.print("Game Chalu Ho Gaya!");
lala.end
```

Compile and run it using the terminal:
```bash
lala game.lala
```

A native, high-performance `.exe` will be generated for you instantly. Enjoy building with Lala SDK!
