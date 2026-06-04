"""Tkinter GUI for the StudentOS AI assistant."""

from __future__ import annotations

import json
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk

try:
    from .chatbot import OllamaError, parse_command
    from .command_executor import CommandExecutionError, CommandExecutor
except ImportError:  # Allows `python chatbot/gui.py`.
    from chatbot import OllamaError, parse_command
    from command_executor import CommandExecutionError, CommandExecutor


class AssistantGUI:
    def __init__(self, root: tk.Tk, base_path: Path | str | None = None) -> None:
        self.root = root
        self.root.title("StudentOS AI Assistant")
        self.root.geometry("960x560")
        self.root.minsize(760, 440)

        self.executor = CommandExecutor(base_path or Path.cwd())
        self.results: queue.Queue[tuple[dict[str, object] | None, str | None, str | None]] = queue.Queue()

        self._build_layout()
        self.root.after(100, self._poll_results)

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.grid(row=0, column=0, sticky="nsew")

        terminal_frame = ttk.Frame(paned, padding=10)
        assistant_frame = ttk.Frame(paned, padding=10)
        paned.add(terminal_frame, weight=1)
        paned.add(assistant_frame, weight=1)

        terminal_frame.columnconfigure(0, weight=1)
        terminal_frame.rowconfigure(1, weight=1)
        assistant_frame.columnconfigure(0, weight=1)
        assistant_frame.rowconfigure(1, weight=1)

        ttk.Label(terminal_frame, text="Terminal").grid(row=0, column=0, sticky="w")
        self.terminal_output = tk.Text(
            terminal_frame,
            wrap="word",
            height=12,
            state="disabled",
            bg="#101418",
            fg="#f2f5f7",
            insertbackground="#f2f5f7",
        )
        self.terminal_output.grid(row=1, column=0, sticky="nsew", pady=(6, 0))

        ttk.Label(assistant_frame, text="AI Assistant").grid(row=0, column=0, sticky="w")
        self.chat_output = tk.Text(assistant_frame, wrap="word", height=12, state="disabled")
        self.chat_output.grid(row=1, column=0, sticky="nsew", pady=(6, 8))

        input_frame = ttk.Frame(assistant_frame)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var)
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.input_entry.bind("<Return>", self._on_send)

        self.send_button = ttk.Button(input_frame, text="Send", command=self._on_send)
        self.send_button.grid(row=0, column=1)
        self.input_entry.focus()

    def _on_send(self, _event: tk.Event | None = None) -> None:
        text = self.input_var.get().strip()
        if not text:
            return

        self.input_var.set("")
        self._append_chat("You", text)
        self._set_busy(True)

        worker = threading.Thread(target=self._run_request, args=(text,), daemon=True)
        worker.start()

    def _run_request(self, text: str) -> None:
        try:
            command = parse_command(text)
            terminal_command = self.executor.to_terminal_command(command)
            result = self.executor.execute(command)
            output = result if not terminal_command else f"$ {terminal_command}\n{result}"
            self.results.put((command, output, None))
        except (OllamaError, CommandExecutionError, OSError) as exc:
            self.results.put((None, None, str(exc)))

    def _poll_results(self) -> None:
        try:
            command, output, error = self.results.get_nowait()
        except queue.Empty:
            self.root.after(100, self._poll_results)
            return

        if error:
            self._append_chat("Assistant", f"Error: {error}")
        elif command is not None and output is not None:
            self._append_chat("Assistant", json.dumps(command, ensure_ascii=False))
            self._append_terminal(output)

        self._set_busy(False)
        self.root.after(100, self._poll_results)

    def _append_chat(self, speaker: str, text: str) -> None:
        self.chat_output.configure(state="normal")
        self.chat_output.insert("end", f"{speaker}: {text}\n\n")
        self.chat_output.see("end")
        self.chat_output.configure(state="disabled")

    def _append_terminal(self, text: str) -> None:
        self.terminal_output.configure(state="normal")
        self.terminal_output.insert("end", f"{text}\n\n")
        self.terminal_output.see("end")
        self.terminal_output.configure(state="disabled")

    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.send_button.configure(state=state)
        self.input_entry.configure(state=state)


def main() -> None:
    root = tk.Tk()
    AssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
