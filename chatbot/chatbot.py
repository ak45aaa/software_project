"""Local Ollama client for turning natural language into commands."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

try:
    from .command_parser import parse_model_response, rule_based_parse
except ImportError:  # Allows `python chatbot.py` during early manual testing.
    from command_parser import parse_model_response, rule_based_parse


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT", "60"))

SYSTEM_PROMPT = """
You are the StudentOS terminal assistant.
Convert the user's natural-language request into exactly one JSON object.
Do not include Markdown, explanations, or extra text.

Supported actions:
- {"action": "create_file", "path": "notes.txt"}
- {"action": "create_folder", "path": "homework"}
- {"action": "delete_file", "path": "notes.txt"}
- {"action": "delete_folder", "path": "homework", "recursive": false}
- {"action": "list_files", "path": "."}
- {"action": "read_file", "path": "notes.txt"}
- {"action": "write_file", "path": "notes.txt", "content": "hello world"}
- {"action": "chat", "message": "short helpful reply"}
- {"action": "change_directory", "path": "homework"}

Rules:
- If the user asks to move into, go to, enter, or change directory, use change_directory.
- Use relative paths only.
- If the user is asking for a terminal/file action, return an action JSON object.
- If the user asks to create a file, use create_file.
- If the user asks to create a folder or directory, use create_folder.
- If the user asks to delete a file, use delete_file.
- If the user asks to delete a folder or directory, use delete_folder.
- If the user asks to show, read, open, or cat a file, use read_file.
- If the user asks to write text into a file, use write_file.
- If the request is not a supported command, return a chat JSON object.
- Never invent unsupported actions.
- Return JSON only.
""".strip()

class OllamaError(RuntimeError):
    """Raised when the local Ollama server cannot return a response."""


def ask_ai(user_text: str) -> str:
    """Ask Ollama for a raw JSON command string."""

    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser request: {user_text}\nJSON:",
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise OllamaError(f"Ollama returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise OllamaError(f"Could not connect to Ollama at {OLLAMA_URL}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise OllamaError("Ollama request timed out.") from exc

    try:
        data: dict[str, Any] = json.loads(body)
    except json.JSONDecodeError as exc:
        raise OllamaError(f"Ollama returned invalid JSON: {body}") from exc

    return str(data.get("response", "")).strip()


def parse_command(user_text: str) -> dict[str, Any]:
    """Return a normalized command dictionary for a user request."""

    direct_command = rule_based_parse(user_text)
    if direct_command is not None:
        return direct_command

    model_text = ask_ai(user_text)
    return parse_model_response(model_text)
