"""CLI entrypoint for the StudentOS AI assistant."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .chatbot import OllamaError, parse_command
    from .command_executor import CommandExecutionError, CommandExecutor
except ImportError:  # Allows `python chatbot/main.py`.
    from chatbot import OllamaError, parse_command
    from command_executor import CommandExecutionError, CommandExecutor


def run_cli() -> None:
    executor = CommandExecutor(Path.cwd())
    print("StudentOS AI Assistant")
    print("Type natural language commands, or 'exit' to quit.")

    while True:
        user_text = input("> ").strip()
        if user_text.lower() in {"exit", "quit"}:
            break
        if not user_text:
            continue

        try:
            command = parse_command(user_text)
            print(json.dumps(command, ensure_ascii=False, indent=2))

            terminal_command = executor.to_terminal_command(command)
            if terminal_command:
                print(f"terminal command: {terminal_command}")

            print(executor.execute(command))
        except (OllamaError, CommandExecutionError, OSError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    run_cli()
