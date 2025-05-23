from master.cvs.commands import AbstractCommand
from master.cvs.service import Printer
from master.cvs.service.handlers import *
from master.cvs.service.objects import CommitMaker
from master.models.command import Merge
from master.models.exceptions import MergeConflictException, MergeException
from master.models.text import *


class MergeCommand(AbstractCommand):
    def __init__(self):
        self.name = Merge.name
        self.description = Merge.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__head_handler = HeadFileHandler(self.__cvs_dir)
        self.__branch_handler = BranchHandler(self.__dir, self.__cvs_dir)
        self.__commit_maker = CommitMaker(self.__cvs_dir)
        self.__file_handler = FileHandler(self.__dir, self.__cvs_dir)
        self.__printer = Printer()

    def get_args(self, parser):
        parser.add_argument(
            "merge_branch",
            type=str
        )

    def run(self, args):
        self._check_repository_initialized()
        merge_branch = args.merge_branch
        target_branch = self.__head_handler.get_current_branch()
        merge_branch_files, target_branch_files = (self
            .__get_files_last_commit_each_branch(
                merge_branch,
                target_branch
            )
        )
        merge_branch_paths = set(merge_branch_files.keys())
        target_branch_paths = set(target_branch_files.keys())
        conflict_files = {}
        new_files = {}
        for path in sorted(merge_branch_paths & target_branch_paths):
            if merge_branch_files[path] != target_branch_files[path]:
                conflict_files[path] = merge_branch_files[path]
        for path in sorted(merge_branch_paths - target_branch_paths):
            new_files[path] = merge_branch_files[path]
        resolved_files = {}
        if conflict_files:
            resolved_files = self.__resolve_conflict(
                conflict_files,
                merge_branch,
                target_branch
            )
        for path, sha1 in resolved_files.items():
            self.__index_handler.add(path, sha1)
        for path, sha1 in new_files.items():
            self.__index_handler.add(path, sha1)
        self.__commit_maker.make_commit(
            MERGE_COMMIT_TEXT.format(
                merge_branch=merge_branch,
                target_branch=target_branch
            )
        )
        commit_sha1 = self.__head_handler.get_head_commit()
        files_to_load = self.__index_handler.get_files_from_commit(commit_sha1)
        self.__file_handler.restore_files_to_directory(
            files_to_load,
            self.__dir
        )
        self.__printer.print_merge_success(
            merge_branch=merge_branch,
            target_branch=target_branch,
            new_files_count=len(new_files),
            resolved_conflicts=len(resolved_files)
        )

    def __get_files_last_commit_each_branch(self, merge_branch, target_branch):
        if merge_branch == target_branch:
            raise MergeException(
                "Merge branch must be different from target branch"
            )
        merge_branch_sha1 = (self.__branch_handler
            .get_head_commit_specified_branch(merge_branch)
        )
        target_branch_sha1 = (self.__branch_handler
            .get_head_commit_specified_branch(target_branch)
        )
        merge_branch_files = self.__index_handler.get_files_from_commit(
            merge_branch_sha1
        )
        target_branch_files = self.__index_handler.get_files_from_commit(
            target_branch_sha1
        )
        return merge_branch_files, target_branch_files

    def __resolve_conflict(self, conflict_files, merge_branch, target_branch):
        resolved_files = {}
        for path, sha1 in conflict_files.items():
            user_input = input(
                MERGE_CONFLICT_TEXT.format(
                    conflict_file=path,
                    merge_branch=merge_branch,
                    target_branch=target_branch
                )
            )
            if user_input == merge_branch:
                resolved_files[path] = sha1
            elif user_input == target_branch:
                continue
            elif user_input == "abort":
                raise MergeConflictException(MERGE_ABORT_TEXT)
            else:
                raise MergeConflictException(
                    "Incorrect input\n" + MERGE_ABORT_TEXT
                )
        return resolved_files
