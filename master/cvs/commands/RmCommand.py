import os

from master.cvs.commands import AbstractCommand
from master.cvs.service.handlers import IndexFileHandler, PathHandler
from master.models.command import Rm


class RmCommand(AbstractCommand):
    def __init__(self):
        self.name = Rm.name
        self.description = Rm.description
        self.__path_handler = PathHandler()
        self.__dir, self.__cvs_dir = self._get_dirs_paths()

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
        index_handler = IndexFileHandler(self.__cvs_dir)
        tracked_files = index_handler.get_index_paths()
        for relative_path in args.paths:
            if args.cached:
                self.__remove_from_index(
                    relative_path,
                    index_handler,
                    tracked_files
                )
            else:
                abs_path = self.__path_handler.make_path(
                    self.__dir,
                    relative_path
                )
                if self.__path_handler.exists(abs_path):
                    if self.__path_handler.is_dir(abs_path):
                        self.__remove_dir(index_handler, abs_path)
                    else:
                        self.__remove_file(
                            index_handler,
                            relative_path,
                            abs_path
                        )
                else:
                    self.__handle_nonexistent_path(
                        relative_path,
                        index_handler,
                        tracked_files
                    )

    @classmethod
    def __remove_from_index(cls, relative_path, idx_handler, tracked_files):
        matched = False
        for tracked_path in tracked_files:
            if (tracked_path == relative_path or
                    tracked_path.startswith(relative_path + os.sep)):
                matched = True
                idx_handler.restore([tracked_path])
        if not matched:
            print(f"\033[91m'{relative_path}' is not tracked\033[0m")

    def __remove_dir(self, index_handler, abs_dir_path):
        for root, _, files in self.__path_handler.walk(abs_dir_path):
            for f in files:
                full_path = self.__path_handler.make_path(root, f)
                rel_path = self.__path_handler.get_rel_path(
                    full_path,
                    self.__dir
                )
                self.__remove_if_tracked(index_handler, rel_path, full_path)
        self.__path_handler.remove_empty_dirs_recursive(abs_dir_path)

    def __remove_file(self, index_handler, relative_path, abs_path):
        self.__remove_if_tracked(index_handler, relative_path, abs_path)
        self.__path_handler.remove_empty_dirs_recursive(
            self.__path_handler.get_dirname(abs_path)
        )

    def __handle_nonexistent_path(self, rel_path, idx_handler, tracked_files):
        matched = False
        for tracked_path in tracked_files:
            if (tracked_path == rel_path or
                    tracked_path.startswith(rel_path + os.sep)):
                matched = True
                self.__remove_if_tracked(idx_handler, tracked_path, None)
        if not matched:
            print(f"\033[91m'{rel_path}' is not tracked\033[0m")

    def __remove_if_tracked(self, index_handler, rel_path, abs_path):
        if index_handler.contains(rel_path):
            if abs_path and self.__path_handler.exists(abs_path):
                self.__path_handler.remove_file(abs_path)
            index_handler.remove(rel_path)
            print(
                f"\033[93mRemoved '{rel_path}' "
                f"from index and directory\033[0m")
        else:
            print(f"\033[91m'{rel_path}' is not tracked\033[0m")
