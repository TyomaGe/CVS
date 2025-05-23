from master.models.command import Init
from master.models.exceptions import RepositoryAlreadyExist
from .AbstractCommand import AbstractCommand
from master.cvs.service.handlers import PathHandler
from ..service.handlers.BranchHandler import BranchHandler


class InitCommand(AbstractCommand):
    def __init__(self):
        self.name = Init.name
        self.description = Init.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__path_handler = PathHandler()
        self.__branch_handler = BranchHandler(self.__dir, self.__cvs_dir)

    def run(self, args):
        self.__init_folder()
        self.__init_cvs_insides()
        print(
            f"\033[92mInitialized empty CVS repository in {self.__dir}\033[0m")

    def __init_folder(self):
        if self.__path_handler.exists(self.__cvs_dir):
            raise RepositoryAlreadyExist("CVS repository already exists")
        self.__path_handler.make_dirs(self.__cvs_dir)
        self.__path_handler.set_hidden(self.__cvs_dir)

    def __init_cvs_insides(self):
        objects_dir = self.__path_handler.make_path(self.__cvs_dir, "objects")
        refs_dir = self.__path_handler.connect_path(self.__cvs_dir, "refs",
                                                    "heads")
        self.__path_handler.make_dirs(objects_dir)
        self.__path_handler.make_dirs(refs_dir)
        self.__branch_handler.change_branch("master")
