class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}


class CannotReadDirectory(Exception):
    def __init__(self, path):
        super().__init__(f"cat: {path}: Is a directory")


class FileSystem:
    def __init__(self, init_dir=None):
        self.root = Directory("/")

        if init_dir is not None:
            self.cwd = init_dir
        else:
            self.cwd = self.root

    def resolve_path(self, current, path):
        if path == "":
            path = "."

        if path.startswith("/"):
            node = self.root
            parts = path.strip("/").split("/")
        else:
            node = current
            parts = path.split("/")

        for part in parts:
            if part == "" or part == ".":
                continue

            elif part == "..":
                if node.parent is not None:
                    node = node.parent

            else:
                if not isinstance(node, Directory):
                    raise NotADirectoryError(path)

                if part not in node.children:
                    raise FileNotFoundError(path)

                node = node.children[part]

        return node

    def pwd(self):
        parts = []
        node = self.cwd

        while node.parent is not None:
            parts.append(node.name)
            node = node.parent

        return "/" + "/".join(reversed(parts))

    def cd(self, path):
        node = self.resolve_path(self.cwd, path)

        if not isinstance(node, Directory):
            raise NotADirectoryError(path)

        self.cwd = node
        return ""

    def ls(self, path=None):
        if path is None:
            node = self.cwd
        else:
            node = self.resolve_path(self.cwd, path)

        if isinstance(node, File):
            return node.name

        return " ".join(node.children.keys())

    def split_parent_name(self, path):
        path = path.rstrip("/")

        if path == "":
            raise ValueError("경로가 비어있습니다")

        parts = path.split("/")
        name = parts[-1]

        parent_path = "/".join(parts[:-1])

        if parent_path == "":
            if path.startswith("/"):
                parent_path = "/"
            else:
                parent_path = "."

        return parent_path, name

    def mkdir(self, path):
        parent_path, name = self.split_parent_name(path)
        parent = self.resolve_path(self.cwd, parent_path)

        if not isinstance(parent, Directory):
            raise NotADirectoryError(parent_path)

        if name in parent.children:
            return f"mkdir: cannot create directory '{path}': File exists"

        parent.children[name] = Directory(name, parent=parent)
        return ""

    def touch(self, path):
        parent_path, name = self.split_parent_name(path)
        parent = self.resolve_path(self.cwd, parent_path)

        if not isinstance(parent, Directory):
            raise NotADirectoryError(parent_path)

        if name not in parent.children:
            parent.children[name] = File(name)

        return ""

    def write_file(self, path, content):
        parent_path, name = self.split_parent_name(path)
        parent = self.resolve_path(self.cwd, parent_path)

        if not isinstance(parent, Directory):
            raise NotADirectoryError(parent_path)

        parent.children[name] = File(name, content)
        return ""

    def rm(self, path):
        parent_path, name = self.split_parent_name(path)
        parent = self.resolve_path(self.cwd, parent_path)

        if name not in parent.children:
            return f"rm: cannot remove '{path}': No such file"

        target = parent.children[name]

        if isinstance(target, Directory):
            return f"rm: cannot remove '{path}': Is a directory"

        del parent.children[name]
        return ""

    def rmdir(self, path):
        parent_path, name = self.split_parent_name(path)
        parent = self.resolve_path(self.cwd, parent_path)

        if name not in parent.children:
            return f"rmdir: failed to remove '{path}': No such directory"

        target = parent.children[name]

        if isinstance(target, File):
            return f"rmdir: failed to remove '{path}': Not a directory"

        if len(target.children) > 0:
            return f"rmdir: failed to remove '{path}': Directory not empty"

        del parent.children[name]
        return ""

    def cat(self, path):
        node = self.resolve_path(self.cwd, path)

        if not isinstance(node, File):
            raise CannotReadDirectory(path)

        return node.content