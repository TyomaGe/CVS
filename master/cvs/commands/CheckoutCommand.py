from master.cvs.commands import AbstractCommand
from master.cvs.service import Printer
from master.cvs.service.handlers import *
from master.models.command import Checkout
from master.models.exceptions import CurrentBranchException


class CheckoutCommand(AbstractCommand):
    def __init__(self):
        self.name = Checkout.name
        self.description = Checkout.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__path_handler = PathHandler()
        self.__file_handler = FileHandler(self.__dir, self.__cvs_dir)
        self.__head_handler = HeadFileHandler(self.__cvs_dir)
        self.__branch_handler = BranchHandler(self.__dir, self.__cvs_dir)
        self.__printer = Printer()

    def get_args(self, parser):
        parser.add_argument(
            "branch",
            type=str,
        )

    def run(self, args):
        self._check_repository_initialized()
        branch_name = args.branch
        self.__branch_handler.branch_exist(branch_name)
        cur_branch = self.__head_handler.get_current_branch()
        if cur_branch == branch_name:
            raise CurrentBranchException(f"Already on branch {branch_name}")
        branch_last_commit_sha1 = (
            self.__branch_handler.get_head_commit_specified_branch(branch_name)
        )
        files = (
            self.__index_handler.get_files_from_commit(branch_last_commit_sha1)
        )
        self.__file_handler.restore_files_to_directory(files, self.__dir)
        self.__index_handler.write_all(files)
        self.__head_handler.change_branch(branch_name)
        print(f"\033[33mSuccessfully switched from"
              f" {cur_branch} to {branch_name}\033[0m")