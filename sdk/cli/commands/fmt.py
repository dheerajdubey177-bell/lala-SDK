import sys
import argparse
from pathlib import Path
from sdk.cli.command import Command
from sdk.project.parser import ProjectParser
from sdk.compiler_api import CompilerAPI

class FmtCommand(Command):
    @property
    def name(self) -> str:
        return "fmt"

    @property
    def help(self) -> str:
        return "Format the current project's source code"

    def execute(self, args: argparse.Namespace):
        cwd = Path.cwd()
        try:
            project = ProjectParser.load(cwd)
        except FileNotFoundError as e:
            print(f"fatal: {e}")
            sys.exit(1)
            
        print(f"Formatting project '{project.package.name}'...")
        
        try:
            results = CompilerAPI.format(project)
            for path, formatted_content in results.items():
                Path(path).write_text(formatted_content)
                print(f"Formatted {path}")
        except Exception as e:
            print(f"fatal: Formatting failed: {e}")
            sys.exit(1)
            
        print("Formatting complete.")

COMMAND = FmtCommand()
