import os
from abc import ABC, abstractmethod
from master.models.exceptions import RepositoryNotInitialized


class AbstractCommand(ABC):
    @abstractmethod
    def run(self, args):
        pass

    @classmethod
    def _check_repository_initialized(cls):
        if not os.path.isdir(os.path.join(os.getcwd(), ".cvs")):
            raise RepositoryNotInitialized(
                "CVS repository is not initialized in this directory"
            )

    @classmethod
    def _get_dirs_paths(cls):
        current_dir = os.getcwd()
        cvs_dir = os.path.join(current_dir, ".cvs")
        return current_dir, cvs_dir

    def get_args(self, parser):
        pass
