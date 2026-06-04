"""Execute validated StudentOS assistant commands safely."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class CommandExecutionError(RuntimeError):
    """Raised when a command cannot be executed safely."""


@dataclass
class CommandExecutor:
    """Execute simple file commands inside a base directory."""

    base_path: Path | str

    def __post_init__(self) -> None:
        self.base_path = Path(self.base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def execute(self, command: dict[str, Any]) -> str:
        action = str(command.get("action", "chat"))

        if action == "chat":
            return str(command.get("message", ""))

        if action == "create_file":
            return self._create_file(command)

        if action == "create_folder":
            path = self._resolve_path(command.get("path"))
            path.mkdir(parents=True, exist_ok=True)
            return f"Created folder: {path.relative_to(self.base_path)}"

        if action == "delete_file":
            path = self._resolve_path(command.get("path"))
            if not path.exists():
                return f"File not found: {path.relative_to(self.base_path)}"
            if not path.is_file():
                raise CommandExecutionError(f"Not a file: {path.relative_to(self.base_path)}")
            path.unlink()
            return f"Deleted file: {path.relative_to(self.base_path)}"

        if action == "delete_folder":
            path = self._resolve_path(command.get("path"))
            if not path.exists():
                return f"Folder not found: {path.relative_to(self.base_path)}"
            if not path.is_dir():
                raise CommandExecutionError(f"Not a folder: {path.relative_to(self.base_path)}")
            if command.get("recursive", False):
                shutil.rmtree(path)
            else:
                path.rmdir()
            return f"Deleted folder: {path.relative_to(self.base_path)}"

        if action == "list_files":
            path = self._resolve_path(command.get("path", "."))
            if not path.exists():
                return f"Folder not found: {path.relative_to(self.base_path)}"
            if not path.is_dir():
                raise CommandExecutionError(f"Not a folder: {path.relative_to(self.base_path)}")
            names = sorted(child.name + ("/" if child.is_dir() else "") for child in path.iterdir())
            return "\n".join(names) if names else "(empty)"

        raise CommandExecutionError(f"Unsupported action: {action}")

    def to_terminal_command(self, command: dict[str, Any]) -> str:
        """Map a structured command to a future StudentOS terminal command string."""

        action = str(command.get("action", "chat"))
        path = str(command.get("path", "."))

        if action == "create_file":
            return f"touch {path}"
        if action == "create_folder":
            return f"mkdir {path}"
        if action == "delete_file":
            return f"rm {path}"
        if action == "delete_folder":
            return f"rm -r {path}" if command.get("recursive", False) else f"rmdir {path}"
        if action == "list_files":
            return f"ls {path}"
        return ""

    def _create_file(self, command: dict[str, Any]) -> str:
        path = self._resolve_path(command.get("path"))
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists() and "content" not in command:
            return f"File already exists: {path.relative_to(self.base_path)}"

        content = command.get("content")
        if content is None:
            path.touch()
        else:
            path.write_text(str(content), encoding="utf-8")

        return f"Created file: {path.relative_to(self.base_path)}"

    def _resolve_path(self, value: Any) -> Path:
        if value is None or str(value).strip() == "":
            raise CommandExecutionError("Missing path.")

        user_path = Path(str(value).strip())
        if user_path.is_absolute():
            raise CommandExecutionError("Absolute paths are not allowed.")

        resolved = (self.base_path / user_path).resolve()
        try:
            resolved.relative_to(self.base_path)
        except ValueError as exc:
            raise CommandExecutionError("Path escapes the StudentOS workspace.") from exc

        return resolved


def execute_command(command: dict[str, Any], base_path: Path | str | None = None) -> str:
    executor = CommandExecutor(base_path or Path.cwd())
    return executor.execute(command)
