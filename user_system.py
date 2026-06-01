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
        print(self.current_user.username)

    def id(self):
        user = self.current_user
        print(f"uid={user.uid}({user.username}) gid={user.gid}({user.username})")

    def users_list(self):
        for username in self.users:
            print(username)

    def userinfo(self):
        user = self.current_user

        print(f"username: {user.username}")
        print(f"uid: {user.uid}")
        print(f"gid: {user.gid}")
        print(f"home: {user.home}")
        print(f"shell: {user.shell}")
        print("password: ********")

    def login(self, username):
        if username not in self.users:
            print(f"login: user '{username}' does not exist")
            return

        password = input("password: ")

        if self.users[username].password != password:
            print("login: incorrect password")
            return

        self.current_user = self.users[username]
        print(f"login success: {username}")

    def passwd(self):
        old_password = input("current password: ")

        if old_password != self.current_user.password:
            print("passwd: authentication failed")
            return

        new_password = input("new password: ")

        if len(new_password) < 4:
            print("passwd: password is too short")
            return

        self.current_user.password = new_password
        print("passwd: password updated successfully")

    def logout(self):
        self.current_user = self.users["user"]
        print("logout: back to user")