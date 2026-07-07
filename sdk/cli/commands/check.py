import sys
import argparse
from pathlib import Path
from sdk.cli.command import Command
from sdk.project.parser import ProjectParser
from sdk.compiler_api import CompilerAPI

class CheckCommand(Command):
    @property
    def name(self) -> str:
        return "check"

    @property
    def help(self) -> str:
        return "Analyze the current project for errors, warnings, and style issues"

    def execute(self, args: argparse.Namespace):
        cwd = Path.cwd()
        try:
            project = ProjectParser.load(cwd)
        except FileNotFoundError as e:
            print(f"fatal: {e}")
            sys.exit(1)
            
        print(f"Checking {project.package.name}...")
        
        diagnostics = CompilerAPI.check(project)
        
        if not diagnostics:
            print("No issues found.")
        else:
            for diag in diagnostics:
                print(diag)

COMMAND = CheckCommand()
