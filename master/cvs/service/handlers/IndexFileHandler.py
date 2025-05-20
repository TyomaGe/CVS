from master.cvs.service import Hashier
from master.cvs.service.handlers.PathHandler import PathHandler
from master.models.exceptions import EmptyIndexException, \
    UnchangedIndexException, HashException


class IndexFileHandler:
    def __init__(self, cvs_dir):
        self.__cvs_dir = cvs_dir
        self.__path_handler = PathHandler()
        self.__index_path = self.__path_handler.make_path(cvs_dir, "index")
        if not self.__path_handler.exists(self.__index_path):
            open(self.__index_path, "w").close()

    def add(self, file_path, sha1):
        entries = self.read()
        entries[file_path] = sha1
        self.write_all(entries)

    def read(self):
        entries = {}
        if self.__path_handler.exists(self.__index_path):
            with open(self.__index_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        path, sha1 = line.rsplit(" ", 1)
                        entries[path] = sha1
        return entries

    def write_all(self, entries):
        with open(self.__index_path, "w") as f:
            for path, sha1 in entries.items():
                f.write(f"{path} {sha1}\n")

    def contains(self, file_path):
        entries = self.read()
        return file_path in entries

    def remove(self, file_path):
        entries = self.read()
        if file_path in entries:
            del entries[file_path]
            self.write_all(entries)

    def get_last_commit_sha1(self):
        head_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "refs",
            "heads",
            "master"
        )
        if not self.__path_handler.exists(head_path):
            return None
        with open(head_path, "r") as f:
            return f.read().strip()

    def get_files_from_commit(self, commit_sha1):
        tree_sha1 = self.get_tree_sha1_from_commit(commit_sha1)
        if not tree_sha1:
            return {}
        files = {}
        self.__walk_tree(tree_sha1, "", files)
        return files

    def get_tree_sha1_from_commit(self, commit_sha1):
        folder, filename = Hashier.get_hash_parts(commit_sha1)
        commit_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "objects",
            folder,
            filename
        )
        if not self.__path_handler.exists(commit_path):
            return None
        with open(commit_path, "rb") as f:
            content = f.read().decode("utf-8")
        for line in content.splitlines():
            if line.startswith("tree "):
                return line.split()[1]
        return None

    def __walk_tree(self, tree_sha1, prefix, files_dict):
        folder, filename = Hashier.get_hash_parts(tree_sha1)
        tree_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "objects",
            folder,
            filename
        )
        if not self.__path_handler.exists(tree_path):
            return
        with open(tree_path, "rb") as f:
            content = f.read().decode("utf-8")
        for line in content.splitlines():
            mode, sha, name = line.split(maxsplit=2)
            path = (self.__path_handler
                    .make_path(prefix, name)) if prefix else name
            if mode == "040000":
                self.__walk_tree(sha, path, files_dict)
            else:
                files_dict[path] = sha

    def has_changes(self):
        current_entries = self.read()
        last_commit_sha1 = self.get_last_commit_sha1()
        if last_commit_sha1:
            last_commit_files = self.get_files_from_commit(last_commit_sha1)
        else:
            last_commit_files = {}
        if not last_commit_sha1 and not current_entries:
            raise EmptyIndexException("Nothing to commit:"
                                      " index is empty and no previous commits")
        if last_commit_sha1 and current_entries == last_commit_files:
            raise UnchangedIndexException("Nothing to commit:"
                                          " index matches the last commit")

    def find_full_commit_sha1(self, short_sha):
        visited = set()
        if len(short_sha) < 7:
            raise HashException("Hash length must be minimum 7 digits")
        current_sha = self.get_last_commit_sha1()
        while current_sha and current_sha not in visited:
            visited.add(current_sha)
            if current_sha.startswith(short_sha):
                return current_sha
            parent_sha = self.__get_parent_commit(current_sha)
            current_sha = parent_sha
        return None

    def __get_parent_commit(self, commit_sha1):
        folder, filename = Hashier.get_hash_parts(commit_sha1)
        commit_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "objects",
            folder,
            filename
        )
        if not self.__path_handler.exists(commit_path):
            return None
        with open(commit_path, "rb") as f:
            content = f.read().decode("utf-8")
        for line in content.splitlines():
            if line.startswith("parent "):
                return line.split()[1]
        return None

    def restore_files_to_directory(self, files_dict, root_dir):
        for rel_path, sha1 in files_dict.items():
            folder, filename = Hashier.get_hash_parts(sha1)
            object_path = self.__path_handler.connect_path(
                self.__cvs_dir, "objects", folder, filename
            )
            if not self.__path_handler.exists(object_path):
                continue
            with open(object_path, "rb") as f:
                content = f.read()
            target_path = self.__path_handler.connect_path(
                root_dir,
                rel_path
            )
            target_dir = self.__path_handler.get_dirname(target_path)
            if not self.__path_handler.exists(target_dir):
                self.__path_handler.make_dirs(target_dir, exist_ok=True)
            with open(target_path, "wb") as out_file:
                out_file.write(content)
            for dirpath, dirnames, filenames in self.__path_handler.walk(
                    root_dir):
                if '.cvs' in dirnames:
                    dirnames.remove('.cvs')
                for filename in filenames:
                    file_rel_path = self.__path_handler.get_rel_path(
                        self.__path_handler.connect_path(dirpath, filename),
                        root_dir
                    )
                    if file_rel_path not in files_dict:
                        self.__path_handler.remove_file(
                            self.__path_handler.connect_path(dirpath,
                                                             filename))

    def update_head(self, commit_sha1, branch_name="master"):
        ref_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "refs",
            "heads",
            branch_name
        )
        with open(ref_path, "w") as f:
            f.write(commit_sha1 + "\n")
