.PHONY: all sdk test clean

all: sdk test

sdk:
	@echo "Building Lala SDK v1.0..."
	@cmd.exe /c build_sdk.bat
	@python tools/install/install.py

test:
	@echo "Running all test suites (including tt / test code)..."
	@python -m unittest discover -s tests -p "test_*.py"

clean:
	@rmdir /s /q build dist bin\__pycache__ 2>nul || true
	@del /q bin\*.exe 2>nul || true
