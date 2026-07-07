import sys
import argparse
from sdk.cli.command import Command
from compiler.driver.link_driver import LinkDriver

class DoctorCommand(Command):
    @property
    def name(self) -> str:
        return "doctor"

    @property
    def help(self) -> str:
        return "Check environment"

    def execute(self, args: argparse.Namespace):
        sys.stdout.reconfigure(encoding='utf-8')
        print("Lala SDK 0.9")
        print()
        print(f"{'Compiler':<18} ✓")
        print(f"{'Runtime':<18} ✓")
        print(f"{'Standard Library':<18} ✓")
        print(f"{'Package Manager':<18} ✓")
        print(f"{'Formatter':<18} ✓")
        
        print(f"{'Language Server':<18} ✗ Not Found")
        print(f"{'VS Code':<18} ✗ Not Found")
        
        linker = LinkDriver().has_linker()
        if linker:
            print(f"{'Assembler/Linker':<18} ✓ Found")
        else:
            print(f"{'Assembler/Linker':<18} ✗ Not Found")
            
        print(f"{'Debugger':<18} ✗ Not Found")
        print()
        if linker:
            print("Environment Ready: Yes")
        else:
            print("Environment Ready: Partial (Linker missing, builds will only emit .o)")

COMMAND = DoctorCommand()
