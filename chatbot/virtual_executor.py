try:
    from .virtual_filesystem import FileSystem, CannotReadDirectory
except ImportError:
    from virtual_filesystem import FileSystem, CannotReadDirectory

class VirtualCommandExecutor:
    def __init__(self):
        self.fs = FileSystem()

    def execute_terminal_command(self, user_input):
        tokens = user_input.strip().split()

        if not tokens:
            return ""

        cmd = tokens[0]
        args = tokens[1:]

        try:
            if cmd == "help":
                return (
                    "--- StudentOS Commands ---\n"
                    "help              : show help\n"
                    "clear             : clear screen\n"
                    "pwd               : print current directory\n"
                    "ls [path]         : list files\n"
                    "cd <path>         : change directory\n"
                    "mkdir <path>      : create directory\n"
                    "touch <path>      : create file\n"
                    "cat <path>        : show file content\n"
                    "echo <text>       : print text\n"
                    "write <file> text : write text to file\n"
                    "rm <path>         : remove file\n"
                    "rmdir <path>      : remove empty directory\n"
                    "exit              : exit program\n"
                    "--------------------------"
                )

            if cmd == "pwd":
                return self.fs.pwd()

            if cmd == "ls":
                path = args[0] if args else None
                return self.fs.ls(path)

            if cmd == "cd":
                if not args:
                    return "cd: missing operand"
                return self.fs.cd(args[0])

            if cmd == "mkdir":
                if not args:
                    return "mkdir: missing operand"
                return self.fs.mkdir(args[0])

            if cmd == "touch":
                if not args:
                    return "touch: missing file operand"
                return self.fs.touch(args[0])

            if cmd == "cat":
                if not args:
                    return "cat: missing file operand"
                return self.fs.cat(args[0])

            if cmd == "echo":
                return " ".join(args)

            if cmd == "write":
                if len(args) < 2:
                    return "write: usage: write <file> <content>"
                path = args[0]
                content = " ".join(args[1:])
                return self.fs.write_file(path, content)

            if cmd == "rm":
                if not args:
                    return "rm: missing operand"
                return self.fs.rm(args[0])

            if cmd == "rmdir":
                if not args:
                    return "rmdir: missing operand"
                return self.fs.rmdir(args[0])

            return f"studentOS: {cmd}: command not found"

        except FileNotFoundError:
            return f"{cmd}: no such file or directory"
        except NotADirectoryError:
            return f"{cmd}: not a directory"
        except CannotReadDirectory as e:
            return str(e)
        except Exception as e:
            return f"Runtime Error: {e}"

    def execute_ai_command(self, command):
        """
        AI가 만든 JSON 명령 실행용.
        예:
        {"action": "create_folder", "path": "test"}
        """

        action = command.get("action")

        try:
            if action == "create_file":
                return self.fs.touch(command.get("path", ""))

            if action == "create_folder":
                return self.fs.mkdir(command.get("path", ""))

            if action == "delete_file":
                return self.fs.rm(command.get("path", ""))

            if action == "delete_folder":
                return self.fs.rmdir(command.get("path", ""))

            if action == "list_files":
                path = command.get("path") or None
                return self.fs.ls(path)

            if action == "read_file":
                return self.fs.cat(command.get("path", ""))

            if action == "write_file":
                return self.fs.write_file(
                    command.get("path", ""),
                    command.get("content", "")
                )

            if action == "chat":
                return command.get("message", "")
            
            if action == "change_directory":
                return self.fs.cd(command.get("path", ""))

            return f"Unknown action: {action}"

        except Exception as e:
            return f"Runtime Error: {e}"

    def to_terminal_command(self, command):
        action = command.get("action")

        if action == "create_file":
            return f"touch {command.get('path', '')}"

        if action == "create_folder":
            return f"mkdir {command.get('path', '')}"

        if action == "delete_file":
            return f"rm {command.get('path', '')}"

        if action == "delete_folder":
            return f"rmdir {command.get('path', '')}"

        if action == "list_files":
            path = command.get("path", "")
            return f"ls {path}".strip()

        if action == "read_file":
            return f"cat {command.get('path', '')}"

        if action == "write_file":
            return f"write {command.get('path', '')} {command.get('content', '')}"

        return ""