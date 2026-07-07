import argparse
from sdk.cli.command import Command

class LearnCommand(Command):
    @property
    def name(self) -> str:
        return "learn"

    @property
    def help(self) -> str:
        return "Interactive Lala learning paths"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("lesson", nargs="?", default="menu", help="Lesson to load (basics, functions, graphics, ai)")

    def execute(self, args: argparse.Namespace):
        print(f"--- Lala Learning Center ---")
        if args.lesson == "menu":
            print("Select a lesson to begin:")
            print("  lala learn basics")
            print("  lala learn functions")
            print("  lala learn graphics")
            print("  lala learn ai")
        elif args.lesson == "basics":
            print("Welcome to Lala Basics!")
            print("In Lala, we use `lala.print(\"Hello World\")` to output text.")
            print("Try writing a program that says Hello World!")
            print("...")
        else:
            print(f"Loading lesson: {args.lesson}...")
            print("Coming soon in Lala v1.0!")

COMMAND = LearnCommand()
