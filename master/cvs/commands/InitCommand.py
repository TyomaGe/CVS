from .AbstractCommand import AbstractCommand
from master.models.command import Init


class InitCommand(AbstractCommand):
    def __init__(self):
        self.name = Init.name
        self.description = Init.description

    def run(self, args):
        print("init run")
