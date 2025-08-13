from abc import ABC, abstractmethod
from master.cvs.service.handlers import PathHandler
from master.models.exceptions import RepositoryNotInitialized


class AbstractCommand(ABC):
    @abstractmethod
    def run(self, args):
        pass

    @staticmethod
    def _check_repository_initialized():
        path_handler = PathHandler()
        cvs_path = path_handler.make_path(path_handler.getcwd(), ".cvs")
        if not path_handler.is_dir(cvs_path):
            raise RepositoryNotInitialized(
                "CVS repository is not initialized in this directory"
            )

    @staticmethod
    def _get_dirs_paths():
        path_handler = PathHandler()
        current_dir = path_handler.getcwd()
        cvs_dir = path_handler.make_path(current_dir, ".cvs")
        return current_dir, cvs_dir

    def get_args(self, parser):
        pass
