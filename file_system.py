class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}  # 이름 -> File 또는 Directory
        
class CannotReadDirectory(Exception):
    def __init__(self, path):
        super().__init__(f"cat: {path}: Is a directory")

class FileSystem:
    def __init__(self, init_dir=None):
        self.root = Directory("/")
        if init_dir != None:
            self.cwd = init_dir
        else:
            self.cwd = self.root
            
    def resolve_path(self, current, path):
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

        print("/" + "/".join(reversed(parts)))
    
    def cd(self, path):
        node = self.resolve_path(self.cwd, path)

        if not isinstance(node, Directory):
            raise NotADirectoryError(path)

        self.cwd = node
        
    def ls(self, path=None):
        if path is None:
            node = self.cwd
        else:
            node = self.resolve_path(self.cwd, path)

        if isinstance(node, File):
            print(node.name)
        else:
            print(" ".join(node.children.keys()))
            
    def split_parent_name(self, path):
        path = path.rstrip("/")

        if path == "":
            raise ValueError("경로가 비어있습니다")

        parts = path.split("/")
        name = parts[-1]

        parent_path = "/".join(parts[:-1])

        if parent_path == "":
            parent_path = "."

        return parent_path, name
            
    def mkdir(self, path):
        parent_path, name = self.split_parent_name(path)
        node = self.resolve_path(self.cwd, parent_path)
        node.children[name] = Directory(name, parent=node)
        
    def touch(self, path):
        parent_path, name = self.split_parent_name(path)
        node = self.resolve_path(self.cwd, parent_path)
        node.children[name] = File(name)
        
    def rm(self, path):
        parent_path, name = self.split_parent_name(path)
        parent = self.resolve_path(self.cwd, parent_path)

        if name not in parent.children:
            print(f"rm: cannot remove '{path}': No such file")
            return

        target = parent.children[name]

        if isinstance(target, Directory):
            print(f"rm: cannot remove '{path}': Is a directory")
            return

        del parent.children[name]
        
    def rmdir(self, path):
        parent_path, name = self.split_parent_name(path)
        parent = self.resolve_path(self.cwd, parent_path)

        if name not in parent.children:
            print(f"rmdir: failed to remove '{path}': No such directory")
            return

        target = parent.children[name]

        if isinstance(target, File):
            print(f"rmdir: failed to remove '{path}': Not a directory")
            return

        if len(target.children) > 0:
            print(f"rmdir: failed to remove '{path}': Directory not empty")
            return

        del parent.children[name]
        
    def cat(self, path):
        node = self.resolve_path(self.cwd, path)
        if not isinstance(node, File):
            raise CannotReadDirectory(path)

        print(node.content)