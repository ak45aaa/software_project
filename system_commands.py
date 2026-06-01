class SystemCommands:
    def __init__(self, user_system, process_manager):
        self.user_system = user_system
        self.process_manager = process_manager

    def execute(self, cmd, args):
        if cmd == "whoami":
            self.user_system.whoami()

        elif cmd == "id":
            self.user_system.id()

        elif cmd == "users":
            self.user_system.users_list()

        elif cmd == "userinfo":
            self.user_system.userinfo()

        elif cmd == "login":
            if len(args) < 1:
                print("login: missing username")
            else:
                self.user_system.login(args[0])

        elif cmd == "logout":
            self.user_system.logout()

        elif cmd == "passwd":
            self.user_system.passwd()

        elif cmd == "ps":
            self.process_manager.ps()

        elif cmd == "top":
            self.process_manager.top()

        elif cmd == "free":
            self.process_manager.free()

        elif cmd == "kill":
            if len(args) < 1:
                print("kill: missing pid")
            else:
                try:
                    pid = int(args[0])
                    self.process_manager.kill(pid)
                except ValueError:
                    print(f"kill: {args[0]}: invalid pid")

        else:
            return False

        return True