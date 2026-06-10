class User:
    def __init__(self, username, password, uid, gid, home, shell):
        self.username = username
        self.password = password
        self.uid = uid
        self.gid = gid
        self.home = home
        self.shell = shell


class UserSystem:
    def __init__(self):
        self.users = {
            "user": User("user", "1234", 1000, 1000, "/home/user", "/bin/pythonOS"),
            "guest": User("guest", "guest", 1001, 1001, "/home/guest", "/bin/pythonOS"),
            "admin": User("admin", "admin", 0, 0, "/root", "/bin/pythonOS"),
        }

        self.current_user = self.users["user"]

    def whoami(self):
        return self.current_user.username

    def id(self):
        user = self.current_user
        return f"uid={user.uid}({user.username}) gid={user.gid}({user.username})"

    def users_list(self):
        return "\n".join(self.users.keys())

    def userinfo(self):
        user = self.current_user

        return (
            f"username: {user.username}\n"
            f"uid: {user.uid}\n"
            f"gid: {user.gid}\n"
            f"home: {user.home}\n"
            f"shell: {user.shell}\n"
            f"password: ********"
        )

    def login(self, username, password):
        if username not in self.users:
            return f"login: user '{username}' does not exist"

        if self.users[username].password != password:
            return "login: incorrect password"

        self.current_user = self.users[username]
        return f"login success: {username}"

    def passwd(self, old_password, new_password):
        if old_password != self.current_user.password:
            return "passwd: authentication failed"

        if len(new_password) < 4:
            return "passwd: password is too short"

        self.current_user.password = new_password
        return "passwd: password updated successfully"

    def logout(self):
        self.current_user = self.users["user"]
        return "logout: back to user"