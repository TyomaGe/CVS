from master.cvs.commands import *


class CommandsFactory:
    @classmethod
    def get_commands(cls):
        return (
            InitCommand,
            AddCommand,
            CommitCommand,
            StatusCommand
        )
