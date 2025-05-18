from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    @abstractmethod
    def run(self, args):
        pass
