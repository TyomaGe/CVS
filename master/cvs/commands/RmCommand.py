from master.cvs.commands import AbstractCommand
from master.cvs.service.handlers import IndexFileHandler, PathHandler
from master.models.command import Rm
from master.models.exceptions import HashException


class RmCommand(AbstractCommand):
    def __init__(self):
        self.name = Rm.name
        self.description = Rm.description
        self.__path_handler = PathHandler()
        self.__dir, self.__cvs_dir = self._get_dirs_paths()

    def get_args(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
        )

    def run(self, args):
        self._check_repository_initialized()
        index_handler = IndexFileHandler(self.__cvs_dir)
        file_path = args.file_path
        if not index_handler.contains(file_path):
            raise HashException(f"File '{file_path}' is not in the index")
        abs_path = self.__path_handler.make_path(self.__dir, file_path)
        self.__path_handler.remove_file(abs_path)
        index_handler.remove(file_path)
        print(
            f"\033[93mFile '{file_path}' removed"
            f" from index and directory\033[0m")
