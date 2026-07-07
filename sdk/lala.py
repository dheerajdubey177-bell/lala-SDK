import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    
from sdk.build_manager import BuildManager
import json

def init_command(args):
    project_name = args.name
    print(f"Initializing Lala project: {project_name}")
    
    dirs = ["src", "tests", "packages", "build", ".lala_cache"]
    for d in dirs:
        os.makedirs(os.path.join(project_name, d), exist_ok=True)
        
    manifest = {
        "name": project_name,
        "version": "0.1.0",
        "language": "0.5",
        "compiler": ">=0.5.0",
        "sdk": "0.5",
        "entry": "src/main.lala",
        "dependencies": {},
        "build": {
            "target": "cpp",
            "optimization": "debug"
        }
    }
    
    with open(os.path.join(project_name, "lala.json"), "w") as f:
        json.dump(manifest, f, indent=2)
        
    with open(os.path.join(project_name, "src", "main.lala"), "w") as f:
        f.write("laao math\n\nlala.print(\"Hello, Lala!\")\n")
        
    print(f"Success! Project {project_name} initialized.")

def build_command(args):
    print("Building Lala project...")
    bm = BuildManager(os.getcwd())
    if bm.build_project():
        print("Build succeeded.")
    else:
        print("Build failed.")
        sys.exit(1)

def run_command(args):
    print("Running Lala project...")
    bm = BuildManager(os.getcwd())
    if bm.build_project():
        import subprocess
        exe_file = os.path.join(os.getcwd(), "build", "main.exe")
        if os.path.exists(exe_file):
            print(f"Executing {exe_file}...")
            subprocess.run([exe_file])
        else:
            print(f"Error: {exe_file} not found after build.")
            sys.exit(1)
    else:
        print("Build failed. Cannot run.")
        sys.exit(1)

def fmt_command(args):
    from tools.formatter.formatter import run_formatter
    if not args.file:
        print("Usage: lala fmt <file>")
        sys.exit(1)
        
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
        
    with open(file_path, "r") as f:
        source_code = f.read()
        
    formatted = run_formatter(source_code)
    
    with open(file_path, "w") as f:
        f.write(formatted)
        
    print(f"Formatted {file_path}")

def lint_command(args):
    from tools.linter.linter import run_linter
    if not args.file:
        print("Usage: lala lint <file>")
        sys.exit(1)
        
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
        
    with open(file_path, "r") as f:
        source_code = f.read()
        
    diagnostics = run_linter(source_code, file_path)
    
    if diagnostics.errors:
        diagnostics.print_diagnostics()
        sys.exit(1)
    else:
        print(f"Linted {file_path}. No issues found.")

def main():
    parser = argparse.ArgumentParser(description="Lala Compiler & Package Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    # Init
    init_parser = subparsers.add_parser("init", help="Initialize a new Lala project")
    init_parser.add_argument("name", help="Name of the project")
    
    # Build
    build_parser = subparsers.add_parser("build", help="Build the current project")
    build_parser.add_argument("--stats", action="store_true", help="Print compiler metrics")
    
    # Run
    run_parser = subparsers.add_parser("run", help="Build and run the current project")
    
    # Check
    check_parser = subparsers.add_parser("check", help="Check the project for errors without building")
    
    # Graph
    graph_parser = subparsers.add_parser("graph", help="Visualize the dependency graph")
    
    # Fmt
    fmt_parser = subparsers.add_parser("fmt", help="Format Lala source code")
    fmt_parser.add_argument("file", help="File to format")
    
    # Lint
    lint_parser = subparsers.add_parser("lint", help="Lint Lala source code")
    lint_parser.add_argument("file", help="File to lint")
    
    # Other placeholders
    subparsers.add_parser("clean", help="Clean the build directory")
    subparsers.add_parser("test", help="Run project tests")
    subparsers.add_parser("doc", help="Generate project documentation")
    subparsers.add_parser("lsp", help="Run the Language Server Protocol (JSON-RPC)")
    subparsers.add_parser("version", help="Print compiler version")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_command(args)
    elif args.command == "build":
        build_command(args)
    elif args.command == "run":
        run_command(args)
    elif args.command == "fmt":
        fmt_command(args)
    elif args.command == "lint":
        lint_command(args)
    elif args.command == "version":
        print("Lala Compiler v0.5.0")
    else:
        print(f"Command '{args.command}' is not yet fully implemented.")

if __name__ == "__main__":
    main()
