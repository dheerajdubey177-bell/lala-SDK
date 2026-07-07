@echo off
echo Building Lala SDK...

REM Install pyinstaller if not present
pip install pyinstaller

REM Build the compiler executable
python -m PyInstaller --onefile bin\lala_compiler.py

REM Copy the executable into the bin folder
copy dist\lala_compiler.exe bin\lala.exe /Y

REM Cleanup pyinstaller build folders
rmdir /s /q build
rmdir /s /q dist
del lala_compiler.spec

echo Build complete! Your SDK is ready in the bin/ folder.
echo You can zip the "bin", "core", and "templates" folders to distribute!
