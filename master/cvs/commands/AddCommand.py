import os

from master.cvs.commands import AbstractCommand
from master.models.command import Add
from master.cvs.service.PathMaker import PathMaker
from master.cvs.service.IndexFileHandler import IndexFileHandler
from master.cvs.service.CVSObjectsMaker import CVSObjectsMaker
from master.models.objects import Blob


class AddCommand(AbstractCommand):
    def __init__(self):
        self.name = Add.name
        self.description = Add.description
        self.__files = None
        self.__dir, self.__cvs_dir = self._get_dirs_paths()

    def run(self, args):
        self.__files = args.files
        path_maker = PathMaker()
        index_handler = IndexFileHandler(self.__cvs_dir)
        object_maker = CVSObjectsMaker(Blob.value, self.__cvs_dir)
        for file in self.__files:
            abs_file_path = path_maker.make_path(self.__dir, file)
            if not os.path.exists(abs_file_path):
                print(f"\033[91mFile '{file}' does not exist\033[0m")
                continue
            sha1 = object_maker.make_object(abs_file_path)
            index_handler.add(file, sha1)

    @classmethod
    def get_args(cls, parser):
        parser.add_argument("files", nargs="+")
