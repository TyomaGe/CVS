from master.cvs.commands import AbstractCommand
from master.cvs.service.handlers import PathHandler, IndexFileHandler
from master.cvs.service.objects import CommitMaker
from master.models.command import Commit


class CommitCommand(AbstractCommand):
    def __init__(self):
        self.name = Commit.name
        self.description = Commit.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__commit_msg = None
        self.__path_handler = PathHandler()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__commit_maker = CommitMaker(self.__cvs_dir)

    def run(self, args):
        self._check_repository_initialized()
        self.__commit_msg = args.message
        self.__index_handler.has_changes()
        sha1 = self.__commit_maker.make_commit(self.__commit_msg)

    @classmethod
    def get_args(cls, parser):
        parser.add_argument(
            "-m", "--message",
            required=True,
            type=str
        )
