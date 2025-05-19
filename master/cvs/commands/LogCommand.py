from master.cvs.commands import AbstractCommand
from master.cvs.service.handlers import HeadFileHandler, PathHandler
from master.cvs.service import Hashier, Printer
from master.models.command import Log


class LogCommand(AbstractCommand):
    def __init__(self):
        self.name = Log.name
        self.description = Log.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__head_handler = HeadFileHandler(self.__cvs_dir)
        self.__path_handler = PathHandler()

    def run(self, args):
        self._check_repository_initialized()
        current_branch = self.__head_handler.get_current_branch()
        head_commit = self.__head_handler.get_head_commit()
        printer = Printer()
        commit_sha1 = head_commit
        while commit_sha1:
            commit_data = self.__read_commit(commit_sha1)
            printer.print_commit(
                commit_sha1,
                commit_data,
                current_branch,
                head_commit
            )
            commit_sha1 = commit_data.get("parent")

    def __read_commit(self, commit_sha):
        folder, filename = Hashier.get_hash_parts(commit_sha)
        commit_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "objects",
            folder,
            filename
        )
        with open(commit_path, "rb") as f:
            content = f.read().decode("utf-8")
        lines = content.splitlines()
        commit_data = {
            "message": lines[-1].strip(),
            "parent": None,
            "author": "anonymous",
            "date": "Unknown"
        }
        for line in lines[:-1]:
            if line.startswith("parent "):
                commit_data["parent"] = line.split()[1]
            elif line.startswith("author "):
                parts = line.split()
                commit_data["author"] = parts[1]
                commit_data["date"] = " ".join(parts[2:8])
        return commit_data
