class SystemCommands:
    def __init__(self, user_system, process_manager):
        self.user_system = user_system
        self.process_manager = process_manager

    def execute(self, cmd, args):
        if cmd == "whoami":
            return self.user_system.whoami()

        elif cmd == "id":
            return self.user_system.id()

        elif cmd == "users":
            return self.user_system.users_list()

        elif cmd == "userinfo":
            return self.user_system.userinfo()

        elif cmd == "login":
            if len(args) < 2:
                return "usage: login <username> <password>"
            return self.user_system.login(args[0], args[1])

        elif cmd == "logout":
            return self.user_system.logout()

        elif cmd == "passwd":
            if len(args) < 2:
                return "usage: passwd <old_password> <new_password>"
            return self.user_system.passwd(args[0], args[1])

        elif cmd == "ps":
            return self.process_manager.ps()

        elif cmd == "top":
            return self.process_manager.top()

        elif cmd == "free":
            return self.process_manager.free()

        elif cmd == "kill":
            if len(args) < 1:
                return "kill: missing pid"

            try:
                pid = int(args[0])
                return self.process_manager.kill(pid)
            except ValueError:
                return f"kill: {args[0]}: invalid pid"

        return None