import os

from master.cvs.commands import AbstractCommand
from master.cvs.service.CVSObjectsMaker import CVSObjectsMaker
from master.cvs.service.IndexFileHandler import IndexFileHandler
from master.cvs.service.PathMaker import PathMaker
from master.models.command import Add
from master.models.objects import Blob


class AddCommand(AbstractCommand):
    def __init__(self):
        self.name = Add.name
        self.description = Add.description
        self.__files = None
        self.__dir, self.__cvs_dir = self._get_dirs_paths()

    def run(self, args):
        self._check_repository_initialized()
        self.__files = args.files
        path_maker = PathMaker()
        index_handler = IndexFileHandler(self.__cvs_dir)
        obj_maker = CVSObjectsMaker(Blob.value, self.__cvs_dir)

        for file in self.__files:
            abs_path = path_maker.make_path(self.__dir, file)
            if not os.path.exists(abs_path):
                print(f"\033[91mPath '{file}' does not exist\033[0m")
                continue
            if os.path.isfile(abs_path):
                self.__add_file(file, abs_path, obj_maker, index_handler)
            else:
                self.__add_directory(abs_path, obj_maker, index_handler,
                                     path_maker)

    @classmethod
    def __add_file(cls, relative_path, abs_path, obj_maker, index_handler):
        sha1 = obj_maker.make_object(abs_path)
        index_handler.add(relative_path, sha1)

    def __add_directory(self, abs_dir, obj_maker, index_handler, path_maker):
        for root, _, files in os.walk(abs_dir):
            for f in files:
                abs_file_path = path_maker.make_path(root, f)
                relative_file_path = os.path.relpath(abs_file_path, self.__dir)
                self.__add_file(relative_file_path, abs_file_path,
                                obj_maker, index_handler)

    @classmethod
    def get_args(cls, parser):
        parser.add_argument("files", nargs="+")
