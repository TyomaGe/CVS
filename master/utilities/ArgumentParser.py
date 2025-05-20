import argparse


class ArgumentParser:
    def __init__(self):
        self.__parser = argparse.ArgumentParser(
            description="CVS - a simple version control system\n"
                        "Use this tool to manage your project files"
                        " with commands like init, add, commit,"
                        " status, log, reset, and rm",
            epilog="Examples:\n"
                   "init\n"
                   "add file.txt\n"
                   "commit -m \"Commit message\"\n"
                   "status",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.__subparsers = self.__parser.add_subparsers(
            dest="command",
            help="Команды CVS"
        )
        self.__command_classes = []

    def register_command(self, CommandClass):
        command_instance = CommandClass()
        command_parser = self.__subparsers.add_parser(
            command_instance.name,
            help=command_instance.description
        )
        command_instance.get_args(command_parser)
        command_parser.set_defaults(command_instance=command_instance)
        self.__command_classes.append(command_instance)

    def get_arguments(self):
        args = self.__parser.parse_args()
        if not hasattr(args, "command_instance"):
            self.__parser.print_help()
            exit(1)
        return args
