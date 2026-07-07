import sys
import argparse
from pathlib import Path
from sdk.cli.command import Command
from sdk.project.parser import ProjectParser
from sdk.compiler_api import CompilerAPI

class BuildCommand(Command):
    @property
    def name(self) -> str:
        return "build"

    @property
    def help(self) -> str:
        return "Compile the current project"

    def execute(self, args: argparse.Namespace):
        cwd = Path.cwd()
        try:
            project = ProjectParser.load(cwd)
        except FileNotFoundError as e:
            print(f"fatal: {e}")
            sys.exit(1)
            
        print(f"Building {project.package.name} v{project.package.version}...")
        
        success, obj_bytes, diagnostics = CompilerAPI.compile(project)
        
        for diag in diagnostics:
            print(diag)
            
        if not success:
            print("Build failed.")
            sys.exit(1)
            
        build_dir = cwd / "build"
        build_dir.mkdir(exist_ok=True)
        
        obj_path = build_dir / f"{project.package.name}.o"
        obj_path.write_bytes(obj_bytes)
        
        print(f"Object emitted to {obj_path}")
        
        from compiler.driver.link_driver import LinkDriver
        driver = LinkDriver()
        if driver.has_linker():
            exe_path = build_dir / f"{project.package.name}.exe"
            try:
                driver.link([str(obj_path)], [], str(exe_path))
                print(f"Successfully linked {exe_path}")
            except Exception as e:
                print(f"Linking failed: {e}")
                sys.exit(1)
        else:
            print("warning: linking skipped (no system linker found).")

COMMAND = BuildCommand()
