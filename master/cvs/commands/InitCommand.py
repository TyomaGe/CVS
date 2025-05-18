import ctypes
import os

from .AbstractCommand import AbstractCommand
from master.models.command import Init
from ..service import HeadFileHandler
from master.models.exceptions import RepositoryAlreadyExist
from ..service.PathMaker import PathMaker


class InitCommand(AbstractCommand):
    def __init__(self):
        self.name = Init.name
        self.description = Init.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()

    def run(self, args):
        self.__init_folder()
        self.__init_cvs_insides()
        print(
            f"\033[92mInitialized empty CVS repository in {self.__dir}\033[0m")

    def __init_folder(self):
        if os.path.exists(self.__cvs_dir):
            raise RepositoryAlreadyExist(
                "CVS repository is already exist"
            )
        os.makedirs(self.__cvs_dir)
        if os.name == 'nt':
            attr_hidden = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(
                self.__cvs_dir,
                attr_hidden
            )

    def __init_cvs_insides(self):
        path_maker = PathMaker()
        objects_dir = path_maker.make_path(self.__cvs_dir, "objects")
        refs_dir = path_maker.connect_path(self.__cvs_dir, "refs", "heads")
        os.makedirs(objects_dir)
        os.makedirs(refs_dir)
        head_path = path_maker.make_path(self.__cvs_dir, "HEAD")
        HeadFileHandler(head_path).change_branch("master")
