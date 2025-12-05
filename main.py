# main.py
# Password Security & Generator CLI
# Created by: Brian Muigai

import sys
from cli import InteractiveCLI

if __name__ == "__main__":
    # Entry point for the password security application
    # Always run interactive mode
    cli = InteractiveCLI()
    cli.run()