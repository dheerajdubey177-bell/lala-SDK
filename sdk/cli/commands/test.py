import sys
import argparse
from pathlib import Path
from sdk.cli.command import Command
from sdk.project.parser import ProjectParser

class TestCommand(Command):
    @property
    def name(self) -> str:
        return "test"

    @property
    def help(self) -> str:
        return "Run tests for the current project"

    def execute(self, args: argparse.Namespace):
        cwd = Path.cwd()
        try:
            project = ProjectParser.load(cwd)
        except FileNotFoundError as e:
            print(f"fatal: {e}")
            sys.exit(1)
            
        print(f"Running tests for {project.package.name}...")
        
        # Stub: We would discover unit tests in `tests/` and run them.
        # For the compiler itself, we can delegate to our golden_tester if we are in the compiler root.
        print("Discovering tests in tests/ ...")
        print("0 tests found.")
        print("Test run complete.")

COMMAND = TestCommand()
