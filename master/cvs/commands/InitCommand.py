import ctypes
import os

from .AbstractCommand import AbstractCommand
from master.models.command import Init
from ..service import HeadFileHandler


class InitCommand(AbstractCommand):
    def __init__(self):
        self.name = Init.name
        self.description = Init.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()

    def run(self, args):
        self.__init_folder()
        self.__init_cvs_insides()

    def __init_folder(self):
        if os.path.exists(self.__cvs_dir):
            print("\033[93mRepository is already initialized\033[0m")
            exit(1)
        os.makedirs(self.__cvs_dir)
        if os.name == 'nt':
            attr_hidden = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(
                self.__cvs_dir,
                attr_hidden
            )
        print(
            f"\033[92mInitialized empty CVS repository in {self.__dir}\033[0m")

    def __init_cvs_insides(self):
        objects_dir = os.path.join(self.__cvs_dir, "objects")
        refs_dir = os.path.join(self.__cvs_dir, "refs", "heads")
        os.makedirs(objects_dir)
        os.makedirs(refs_dir)
        head_path = os.path.join(self.__cvs_dir, "HEAD")
        HeadFileHandler(head_path).change_branch("master")
