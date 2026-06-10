"""Tkinter GUI for the StudentOS AI assistant + interactive terminal."""

from __future__ import annotations

import json
import queue
import threading
import tkinter as tk
from tkinter import ttk

try:
    from .chatbot import parse_command as ai_parse_command
    from .virtual_executor import VirtualCommandExecutor
except ImportError:
    from chatbot import parse_command as ai_parse_command
    from virtual_executor import VirtualCommandExecutor


class AssistantGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("StudentOS AI Assistant")
        self.root.geometry("960x560")
        self.root.minsize(760, 440)

        self.executor = VirtualCommandExecutor()

        self.results: queue.Queue[
            tuple[dict[str, object] | None, str | None, str | None]
        ] = queue.Queue()

        self.prompt = "user@pythonOS:~$ "

        self._build_layout()
        self._start_terminal()

        self.root.after(100, self._poll_results)
        
    def _get_prompt(self) -> str:
        username = self.executor.user_system.current_user.username
        path = self.executor.fs.pwd()

        if path == "/":
            display_path = "/"
        elif path == self.executor.user_system.current_user.home:
            display_path = "~"
        elif path.startswith(self.executor.user_system.current_user.home + "/"):
            display_path = "~" + path[len(self.executor.user_system.current_user.home):]
        else:
            display_path = path

        return f"{username}@pythonOS:{display_path}$ "

    # ==========================================
    # 1. GUI 레이아웃
    # ==========================================
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
            bg="#101418",
            fg="#f2f5f7",
            insertbackground="#f2f5f7",
            font=("Courier New", 12),
            borderwidth=0,
            highlightthickness=0,
        )
        self.terminal_output.grid(row=1, column=0, sticky="nsew", pady=(6, 0))

        self.terminal_output.bind("<Return>", self._on_terminal_enter)
        self.terminal_output.bind("<BackSpace>", self._protect_prompt_backspace)

        ttk.Label(assistant_frame, text="AI Assistant").grid(row=0, column=0, sticky="w")

        self.chat_output = tk.Text(
            assistant_frame,
            wrap="word",
            height=12,
            state="disabled",
        )
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

    # ==========================================
    # 2. 터미널 출력 관련
    # ==========================================
    def _start_terminal(self) -> None:
        self._terminal_writeln("Welcome to Python OS (v1.0)")
        self._terminal_writeln("Type 'help' to see available commands.")
        self._terminal_writeln("")
        self._write_prompt()
        self.terminal_output.focus()

    def _terminal_write(self, text: str) -> None:
        self.terminal_output.insert("end", text)
        self.terminal_output.see("end")

    def _terminal_writeln(self, text: str = "") -> None:
        self._terminal_write(text + "\n")

    def _write_prompt(self) -> None:
        self.prompt = self._get_prompt()
        self._terminal_write(self.prompt)
        self.terminal_output.mark_set("insert", "end")

    def _clear_terminal(self) -> None:
        self.terminal_output.delete("1.0", "end")

    # ==========================================
    # 4. 일반 터미널 명령어 실행
    # ==========================================
    def _execute_terminal_command(self, user_input: str) -> None:
        cmd = user_input.strip().split()[0] if user_input.strip() else ""

        if cmd == "clear":
            self._clear_terminal()
            return

        if cmd == "exit":
            self._terminal_writeln("Logout. Goodbye!")
            self.root.quit()
            return

        result = self.executor.execute_terminal_command(user_input)

        if result:
            self._terminal_writeln(result)

    def _on_terminal_enter(self, event: tk.Event | None = None) -> str:
        current_line = self.terminal_output.get("insert linestart", "end-1c")

        if current_line.startswith(self.prompt):
            user_input = current_line[len(self.prompt):].strip()
        else:
            user_input = ""

        self._terminal_write("\n")
        self._execute_terminal_command(user_input)
        self._write_prompt()

        return "break"

    def _protect_prompt_backspace(self, event: tk.Event | None = None) -> str | None:
        current_line = self.terminal_output.get("insert linestart", "insert")

        if current_line == self.prompt:
            return "break"

        return None

    # ==========================================
    # 5. AI Assistant 입력 처리
    # ==========================================
    def _on_send(self, _event: tk.Event | None = None) -> None:
        text = self.input_var.get().strip()

        if not text:
            return

        self.input_var.set("")
        self._append_chat("You", text)
        self._set_busy(True)

        worker = threading.Thread(target=self._run_ai_request, args=(text,), daemon=True)
        worker.start()

    def _run_ai_request(self, text: str) -> None:
        try:
            command = ai_parse_command(text)

            terminal_command = self.executor.to_terminal_command(command)
            result = self.executor.execute_ai_command(command)

            if terminal_command:
                output = f"$ {terminal_command}\n{result}"
            else:
                output = result

            self.results.put((command, output, None))

        except Exception as exc:
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
            self._terminal_writeln("")
            self._terminal_writeln(output)
            self._write_prompt()

        self._set_busy(False)
        self.root.after(100, self._poll_results)

    # ==========================================
    # 6. 채팅창 출력
    # ==========================================
    def _append_chat(self, speaker: str, text: str) -> None:
        self.chat_output.configure(state="normal")
        self.chat_output.insert("end", f"{speaker}: {text}\n\n")
        self.chat_output.see("end")
        self.chat_output.configure(state="disabled")

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