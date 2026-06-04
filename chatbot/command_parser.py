"""Parse and validate AI-produced StudentOS commands."""

from __future__ import annotations

import json
import re
from json import JSONDecodeError
from typing import Any


ALLOWED_ACTIONS = {
    "create_file",
    "create_folder",
    "delete_file",
    "delete_folder",
    "list_files",
    "chat",
}

ACTION_ALIASES = {
    "mkdir": "create_folder",
    "create_dir": "create_folder",
    "create_directory": "create_folder",
    "new_folder": "create_folder",
    "touch": "create_file",
    "new_file": "create_file",
    "remove_file": "delete_file",
    "rm_file": "delete_file",
    "remove_folder": "delete_folder",
    "remove_dir": "delete_folder",
    "delete_dir": "delete_folder",
    "delete_directory": "delete_folder",
    "ls": "list_files",
    "dir": "list_files",
    "list_dir": "list_files",
}

REQUIRES_PATH = {
    "create_file",
    "create_folder",
    "delete_file",
    "delete_folder",
}


def parse_model_response(text: str) -> dict[str, Any]:
    """Extract one JSON command from model text and normalize it."""

    data = extract_json_object(text)
    if data is None:
        return chat_command(text.strip() or "I could not understand that request.")
    return normalize_command(data)


def normalize_command(data: Any) -> dict[str, Any]:
    """Return a safe command dictionary with predictable keys."""

    if not isinstance(data, dict):
        return chat_command("I could not understand that request.")

    action = str(data.get("action", "chat")).strip().lower()
    action = ACTION_ALIASES.get(action, action)

    if action not in ALLOWED_ACTIONS:
        return chat_command(str(data.get("message") or "Unsupported command."))

    if action == "chat":
        return chat_command(str(data.get("message") or data.get("response") or ""))

    path = _clean_path(data.get("path"))
    if action in REQUIRES_PATH and not path:
        return chat_command(f"The {action} command needs a path.")

    command: dict[str, Any] = {"action": action}
    if path:
        command["path"] = path

    if action == "list_files" and not path:
        command["path"] = "."

    if action == "create_file" and "content" in data:
        command["content"] = str(data.get("content") or "")

    if action == "delete_folder":
        command["recursive"] = bool(data.get("recursive", False))

    return command


def extract_json_object(text: str) -> dict[str, Any] | None:
    """Find and decode the first JSON object in a string."""

    stripped = text.strip()
    if not stripped:
        return None

    try:
        value = json.loads(stripped)
    except JSONDecodeError:
        value = None

    if isinstance(value, dict):
        return value

    decoder = json.JSONDecoder()
    for index, char in enumerate(stripped):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(stripped[index:])
        except JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value

    return None


def rule_based_parse(user_text: str) -> dict[str, Any] | None:
    """Handle common simple commands without needing an LLM call."""

    text = user_text.strip()
    if not text:
        return chat_command("")

    patterns: list[tuple[str, str]] = [
        (r"^(?:create|make|new)\s+(?:a\s+)?(?:file|text file)\s+(?:called|named)?\s*(.+)$", "create_file"),
        (r"^(?:create|make|new)\s+(?:a\s+)?(?:folder|directory|dir)\s+(?:called|named)?\s*(.+)$", "create_folder"),
        (r"^(?:delete|remove)\s+(?:the\s+)?file\s+(.+)$", "delete_file"),
        (r"^(?:delete|remove)\s+(?:the\s+)?(?:folder|directory|dir)\s+(.+)$", "delete_folder"),
    ]

    for pattern, action in patterns:
        match = re.match(pattern, text, flags=re.IGNORECASE)
        if match:
            path = _clean_path(match.group(1))
            if path:
                return {"action": action, "path": path}

    list_match = re.match(
        r"^(?:list|show)\s+(?:the\s+)?(?:files|folders|directory|dir)"
        r"(?:\s+(?:in|inside|from)\s+(.+))?$",
        text,
        flags=re.IGNORECASE,
    )
    if list_match:
        return {"action": "list_files", "path": _clean_path(list_match.group(1)) or "."}

    return None


def chat_command(message: str) -> dict[str, str]:
    return {"action": "chat", "message": message}


def _clean_path(value: Any) -> str:
    if value is None:
        return ""

    path = str(value).strip()
    path = path.strip("\"'")
    path = re.sub(r"\s+", " ", path)
    return path
