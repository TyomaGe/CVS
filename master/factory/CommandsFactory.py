from master.cvs.commands import *
from master.cvs.commands.RmCommand import RmCommand


class CommandsFactory:
    @classmethod
    def get_commands(cls):
        return (
            InitCommand,
            AddCommand,
            CommitCommand,
            StatusCommand,
            LogCommand,
            ResetCommand,
            RmCommand
        )
