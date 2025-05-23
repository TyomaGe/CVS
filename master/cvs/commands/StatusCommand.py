from master.cvs.commands import AbstractCommand
from master.cvs.service import Printer, Hashier
from master.cvs.service.handlers import *
from master.models.command import Status


class StatusCommand(AbstractCommand):
    def __init__(self):
        self.name = Status.name
        self.description = Status.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__head_handler = HeadFileHandler(self.__cvs_dir)
        self.__path_handler = PathHandler()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__printer = Printer()

    def run(self, args):
        self._check_repository_initialized()
        current_branch = self.__head_handler.get_current_branch()
        staged_changes = self.__get_staged_changes()
        unstaged_changes = self.__get_unstaged_changes()
        self.__printer.print_status(
            current_branch,
            staged_changes,
            unstaged_changes
        )

    def __get_staged_changes(self):
        last_commit_sha = self.__index_handler.get_last_commit_sha1()
        if not last_commit_sha:
            return {"new file": list(self.__index_handler.read().keys())}
        last_commit_files = self.__index_handler.get_files_from_commit(
            last_commit_sha)
        current_index = self.__index_handler.read()
        changes = {"modified": [], "new file": [], "deleted": []}
        for file, index_sha in current_index.items():
            if file not in last_commit_files:
                changes["new file"].append(file)
            elif last_commit_files[file] != index_sha:
                changes["modified"].append(file)
        for file in last_commit_files:
            if file not in current_index:
                changes["deleted"].append(file)
        return {k: v for k, v in changes.items() if v}

    def __get_unstaged_changes(self):
        index_entries = self.__index_handler.read()
        changes = {"modified": [], "deleted": []}
        for file, index_sha in index_entries.items():
            file_path = self.__path_handler.make_path(self.__dir, file)
            if not self.__path_handler.exists(file_path):
                changes["deleted"].append(file)
                continue
            if self.__path_handler.is_file(file_path):
                current_sha = Hashier.hash_file(file_path)
                if current_sha != index_sha:
                    changes["modified"].append(file)
        return changes
