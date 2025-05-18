import os
from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    @abstractmethod
    def run(self, args):
        pass

    @classmethod
    def _check_repository_initialized(cls):
        if not os.path.isdir(os.path.join(os.getcwd(), ".cvs")):
            print("\033[91mError: CVS repository not initialized in this directory.\033[0m")
            exit(1)
