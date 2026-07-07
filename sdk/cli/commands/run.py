import sys
import argparse
import subprocess
from pathlib import Path
from sdk.cli.command import Command
from sdk.project.parser import ProjectParser

class RunCommand(Command):
    @property
    def name(self) -> str:
        return "run"

    @property
    def help(self) -> str:
        return "Build and execute the current project"

    def execute(self, args: argparse.Namespace):
        # We can just delegate to build, then execute
        from sdk.cli.commands.build import COMMAND as build_cmd
        build_cmd.execute(args)
        
        cwd = Path.cwd()
        project = ProjectParser.load(cwd)
        exe_path = cwd / "build" / f"{project.package.name}.exe"
        
        if exe_path.exists():
            subprocess.run([str(exe_path)])
        else:
            print("Cannot run (no executable generated).")

COMMAND = RunCommand()
