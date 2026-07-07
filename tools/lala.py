import sys
import argparse
from pathlib import Path

# Add project root to PYTHONPATH so we can import compiler/sdk
sys.path.insert(0, str(Path(__file__).parent.parent))

from sdk.cli.registry import CommandRegistry

def main():
    parser = argparse.ArgumentParser(prog="lala", description="The Lala SDK DX Platform")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    registry = CommandRegistry()
    registry.discover("sdk.cli.commands")
    
    for cmd in registry.get_commands():
        cmd_parser = subparsers.add_parser(cmd.name, help=cmd.help)
        cmd.add_arguments(cmd_parser)
        cmd_parser.set_defaults(func=cmd.execute)
        
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
