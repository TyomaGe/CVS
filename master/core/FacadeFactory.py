from master.factory import CommandsFactory


class FacadeFactory:
    def __init__(self, parser):
        self.__commands = CommandsFactory.get_commands()
        self.__parser = parser

    def register_commands(self):
        for command in self.__commands:
            self.__parser.register_command(command)
