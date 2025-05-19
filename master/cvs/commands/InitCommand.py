from master.models.command import Init
from master.models.exceptions import RepositoryAlreadyExist
from .AbstractCommand import AbstractCommand
from ..service import HeadFileHandler
from ..service.PathHandler import PathHandler


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
        path_handler = PathHandler()
        if path_handler.exists(self.__cvs_dir):
            raise RepositoryAlreadyExist("CVS repository already exists")
        path_handler.make_dirs(self.__cvs_dir)
        path_handler.set_hidden(self.__cvs_dir)

    def __init_cvs_insides(self):
        path_handler = PathHandler()
        objects_dir = path_handler.make_path(self.__cvs_dir, "objects")
        refs_dir = path_handler.connect_path(self.__cvs_dir, "refs", "heads")
        path_handler.make_dirs(objects_dir)
        path_handler.make_dirs(refs_dir)
        head_path = path_handler.make_path(self.__cvs_dir, "HEAD")
        HeadFileHandler(head_path).change_branch("master")
