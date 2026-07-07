import sys
import argparse
from pathlib import Path
from sdk.cli.command import Command
from sdk.project.parser import ProjectParser
from sdk.docgen.model import DocGenerator

class DocCommand(Command):
    @property
    def name(self) -> str:
        return "doc"

    @property
    def help(self) -> str:
        return "Generate documentation for the project"

    def execute(self, args: argparse.Namespace):
        cwd = Path.cwd()
        try:
            project = ProjectParser.load(cwd)
        except FileNotFoundError as e:
            print(f"fatal: {e}")
            sys.exit(1)
            
        print(f"Generating documentation for {project.package.name}...")
        
        # Stub: We would generate documentation based on AST docstrings
        docs_dir = cwd / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        html_content = f"<html><head><title>{project.package.name} Docs</title></head><body><h1>{project.package.name} v{project.package.version}</h1></body></html>"
        (docs_dir / "index.html").write_text(html_content)
        
        print(f"Documentation generated at {docs_dir}/index.html")

COMMAND = DocCommand()
