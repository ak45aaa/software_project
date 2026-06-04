"""StudentOS local AI assistant package."""

from .chatbot import OllamaError, ask_ai, parse_command
from .command_executor import CommandExecutor, execute_command

__all__ = [
    "CommandExecutor",
    "OllamaError",
    "ask_ai",
    "execute_command",
    "parse_command",
]
