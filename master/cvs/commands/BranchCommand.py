from select import select

from master.cvs.commands import AbstractCommand
from master.cvs.service import Printer
from master.cvs.service.handlers import *
from master.models.command import Branch
from master.models.exceptions import *


class BranchCommand(AbstractCommand):
    def __init__(self):
        self.name = Branch.name
        self.description = Branch.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__path_handler = PathHandler()
        self.__file_handler = FileHandler(self.__dir, self.__cvs_dir)
        self.__head_handler = HeadFileHandler(self.__cvs_dir)
        self.__branch_handler = BranchHandler(self.__dir, self.__cvs_dir)
        self.__printer = Printer()

    def get_args(self, parser):
        parser.add_argument(
            "name",
            type=str,
            nargs="?",
            default=None,

        )
        parser.add_argument(
            "-d", "--delete",
            action="store_true",
        )

    def run(self, args):
        self._check_repository_initialized()
        branch_name = args.name
        is_to_delete = args.delete
        if branch_name and is_to_delete:
            self.__delete_branch(branch_name)
        elif branch_name:
            self.__create_branch(branch_name)
        else:
            self.__print_branch_list()

    def __delete_branch(self, branch_name):
        self.__branch_handler.branch_exist(branch_name)
        cur_branch = self.__head_handler.get_current_branch()
        if cur_branch == branch_name:
            raise CurrentBranchException(
                f"To delete branch {branch_name} you have to"
                f" checkout to another branch"
            )
        if cur_branch == "master":
            raise MasterBranchException("Can`t delete master branch")
        branch_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "refs",
            "heads",
            branch_name
        )
        self.__path_handler.remove_file(branch_path)
        print(f"\033[33mSuccessfully deleted branch {branch_name}\033[0m")

    def __create_branch(self, branch_name):
        last_commit_sha1 = self.__index_handler.get_last_commit_sha1()
        branch_list = self.__branch_handler.get_branch_list()
        if branch_name in branch_list:
            raise CurrentBranchException(f"Branch {branch_name} already exist")
        if not last_commit_sha1:
            raise BranchHasNoCommits("The last commit was not found")
        else:
            branch_dir = self.__path_handler.connect_path(
                self.__cvs_dir,
                "refs",
                "heads",
                branch_name
            )
            with open(branch_dir, "w") as f:
                f.write(last_commit_sha1)
            print(f"\033[92mSuccessfully created "
                  f"branch {branch_name}\033[0m")

    def __print_branch_list(self):
        branches = self.__branch_handler.get_branch_list()
        cur_branch = self.__head_handler.get_current_branch()
        self.__printer.print_branch_list(branches, cur_branch)
