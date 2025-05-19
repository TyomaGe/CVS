from master.cvs.commands import AbstractCommand
from master.cvs.service.StatusPrinter import StatusPrinter
from master.cvs.service.handlers import IndexFileHandler, PathHandler
from master.cvs.service import Hashier
from master.models.command import Status


class StatusCommand(AbstractCommand):
    def __init__(self):
        self.name = Status.name
        self.description = Status.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__path_handler = PathHandler()

    def run(self, args):
        self._check_repository_initialized()
        current_branch = self.__get_current_branch()
        index_handler = IndexFileHandler(self.__cvs_dir)
        staged_changes = self.__get_staged_changes(index_handler)
        unstaged_changes = self.__get_unstaged_changes(index_handler)
        status_printer = StatusPrinter()
        status_printer.print_status(
            current_branch,
            staged_changes,
            unstaged_changes
        )

    def __get_current_branch(self):
        head_path = self.__path_handler.connect_path(self.__cvs_dir, "HEAD")
        with open(head_path, "r") as f:
            ref = f.read().strip()
            return ref[len("refs/heads/"):]

    @classmethod
    def __get_staged_changes(cls, index_handler):
        last_commit_sha = index_handler.get_last_commit_sha1()
        if not last_commit_sha:
            return {"new file": list(index_handler.read().keys())}
        last_commit_files = index_handler.get_files_from_commit(
            last_commit_sha)
        current_index = index_handler.read()
        changes = {"modified": [], "new file": []}
        for file, index_sha in current_index.items():
            if file not in last_commit_files:
                changes["new file"].append(file)
            elif last_commit_files[file] != index_sha:
                changes["modified"].append(file)
        return {k: v for k, v in changes.items() if v}

    def __get_unstaged_changes(self, index_handler):
        index_entries = index_handler.read()
        changes = {"modified": [], "deleted": []}
        for file, index_sha in index_entries.items():
            file_path = self.__path_handler.make_path(self.__dir, file)
            if self.__path_handler.is_file(file_path):
                current_sha = Hashier.hash_file(file_path)
                if current_sha != index_sha:
                    changes["modified"].append(file)
        return changes
