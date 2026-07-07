import sys
import argparse
from pathlib import Path
from sdk.cli.command import Command

class NewCommand(Command):
    @property
    def name(self) -> str:
        return "new"

    @property
    def help(self) -> str:
        return "Create a new Lala project"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("name", help="Name of the project")

    def execute(self, args: argparse.Namespace):
        project_dir = Path.cwd() / args.name
        if project_dir.exists():
            print(f"fatal: Directory '{args.name}' already exists.")
            sys.exit(1)
            
        project_dir.mkdir()
        (project_dir / "src").mkdir()
        (project_dir / "tests").mkdir()
        
        toml_content = f"""[package]
name = "{args.name}"
version = "0.1.0"
edition = "2026"

[dependencies]

[build]
optimization = "O0"
target = "x86_64"
entry = "lala.main"
"""
        (project_dir / "lala.toml").write_text(toml_content)
        
        main_content = """lala.kaam main():
    print("Hello, Lala!")
"""
        (project_dir / "src" / "main.lala").write_text(main_content)
        
        print(f"Created new project `{args.name}`")

COMMAND = NewCommand()
