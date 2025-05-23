from master.cvs.commands import AbstractCommand
from master.cvs.service.objects import BlobMaker
from master.cvs.service.handlers import IndexFileHandler, PathHandler
from master.models.command import Add


class AddCommand(AbstractCommand):
    def __init__(self):
        self.name = Add.name
        self.description = Add.description
        self.__files = None
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__path_handler = PathHandler()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__blob_maker = BlobMaker(self.__cvs_dir)

    def run(self, args):
        self._check_repository_initialized()
        self.__files = args.files

        for file in self.__files:
            abs_path = self.__path_handler.make_path(self.__dir, file)
            if not self.__path_handler.exists(abs_path):
                print(f"\033[91mPath '{file}' does not exist\033[0m")
                continue

            if self.__path_handler.is_file(abs_path):
                self.__add_file(file, abs_path)
            else:
                self.__add_directory(abs_path)

    def __add_file(self, relative_path, abs_path):
        sha1 = self.__blob_maker.make_blob(abs_path)
        self.__index_handler.add(relative_path, sha1)

    def __add_directory(self, abs_dir):
        for root, _, files in self.__path_handler.walk(abs_dir):
            for f in files:
                abs_file_path = self.__path_handler.make_path(root, f)
                relative_file_path = self.__path_handler.get_rel_path(
                    abs_file_path,
                    self.__dir
                )
                self.__add_file(relative_file_path, abs_file_path)

    @classmethod
    def get_args(cls, parser):
        parser.add_argument("files", nargs="+")
