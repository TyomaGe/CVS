from master.cvs.commands import AbstractCommand
from master.cvs.service.handlers import IndexFileHandler, PathHandler
from master.cvs.service.handlers.FileHandler import FileHandler
from master.models.command import Rm


class RmCommand(AbstractCommand):
    def __init__(self):
        self.name = Rm.name
        self.description = Rm.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__path_handler = PathHandler()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__file_handler = FileHandler(self.__dir, self.__cvs_dir)

    def get_args(self, parser):
        parser.add_argument(
            "paths",
            nargs="+",
        )
        parser.add_argument(
            "--cached",
            action="store_true"
        )

    def run(self, args):
        self._check_repository_initialized()
        tracked_files = self.__index_handler.get_index_paths()
        for relative_path in args.paths:
            if args.cached:
                self.__file_handler.remove_from_index(
                    relative_path,
                    self.__index_handler,
                    tracked_files
                )
            else:
                abs_path = self.__path_handler.make_path(
                    self.__dir,
                    relative_path
                )
                if self.__path_handler.exists(abs_path):
                    if self.__path_handler.is_dir(abs_path):
                        self.__file_handler.remove_dir(self.__index_handler,
                                                       abs_path)
                    else:
                        self.__file_handler.remove_file(
                            self.__index_handler,
                            relative_path,
                            abs_path
                        )
                else:
                    self.__file_handler.handle_nonexistent_path(
                        relative_path,
                        self.__index_handler,
                        tracked_files
                    )
