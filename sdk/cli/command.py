from abc import ABC, abstractmethod
import argparse

class Command(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        pass

    def add_arguments(self, parser: argparse.ArgumentParser):
        """Override to add command-specific arguments."""
        pass

    @abstractmethod
    def execute(self, args: argparse.Namespace):
        """Execute the command."""
        pass
