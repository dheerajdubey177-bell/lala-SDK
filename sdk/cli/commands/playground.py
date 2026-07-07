import sys
import argparse
from sdk.cli.command import Command
from sdk.language_service.playground.server import PlaygroundServer
import json

class PlaygroundCommand(Command):
    @property
    def name(self) -> str:
        return "playground"

    @property
    def help(self) -> str:
        return "Launch the local web playground backend API stub"

    def execute(self, args: argparse.Namespace):
        print("Lala Web Playground Backend running on port 8080 (Stub)", file=sys.stderr)
        server = PlaygroundServer()
        
        # Stub to represent it running, we won't implement a real HTTP server here
        # just print and return.
        print("Waiting for connections...")

COMMAND = PlaygroundCommand()
