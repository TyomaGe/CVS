from master.core.FacadeFactory import FacadeFactory
from master.utilities.ArgumentParser import ArgumentParser


def main():
    parser = ArgumentParser()
    facade_factory = FacadeFactory(parser)
    facade_factory.register_commands()
    args = parser.get_arguments()
    args.command_instance.run(args)
