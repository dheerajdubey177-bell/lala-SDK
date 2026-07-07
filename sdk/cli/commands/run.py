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
        cwd = Path.cwd()
        try:
            project = ProjectParser.load(cwd)
        except FileNotFoundError as e:
            print(f"fatal: {e}")
            sys.exit(1)
            
        print(f"Running {project.package.name} v{project.package.version}...")
        
        if not project.source_files:
            print("No source files found.")
            sys.exit(1)
            
        source = project.source_files[0].content
        
        from compiler.frontend.lexer import Lexer
        from compiler.frontend.parser import Parser
        from compiler.backend.interpreter import Interpreter
        try:
            tokens = Lexer(source).tokenize()
            ast = Parser(tokens, "<memory>").parse()
            res = Interpreter().evaluate(ast)
            sys.exit(res if isinstance(res, int) else 0)
        except Exception as e:
            print(f"Runtime error: {e}")
            sys.exit(1)

COMMAND = RunCommand()
