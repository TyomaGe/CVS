from master.cvs.commands import *
from master.cvs.commands.AddCommand import AddCommand


class CommandsFactory:
    @classmethod
    def get_commands(cls):
        return (
            InitCommand,
            AddCommand,
        )
