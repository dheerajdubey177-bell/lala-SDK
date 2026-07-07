from typing import Dict, List
from .command import Command
import pkgutil
import importlib

class CommandRegistry:
    def __init__(self):
        self._commands: Dict[str, Command] = {}

    def register(self, command: Command):
        self._commands[command.name] = command

    def get_commands(self) -> List[Command]:
        return list(self._commands.values())
        
    def discover(self, package_name: str):
        """
        Dynamically discover and load commands from a package.
        """
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            return
            
        for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
            if not is_pkg:
                full_module_name = f"{package_name}.{module_name}"
                module = importlib.import_module(full_module_name)
                # Look for a COMMAND variable exposing the command
                if hasattr(module, "COMMAND"):
                    self.register(module.COMMAND)
