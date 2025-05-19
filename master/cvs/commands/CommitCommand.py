from master.cvs.commands import AbstractCommand
from master.cvs.service.handlers import PathHandler
from master.cvs.service.objects import CVSObjectsMaker
from master.models.command import Commit


class CommitCommand(AbstractCommand):
    def __init__(self):
        self.name = Commit.name
        self.description = Commit.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__commit_msg = None
        self.__path_handler = PathHandler()

    def run(self, args):
        self._check_repository_initialized()
        self.__commit_msg = args.message
        objects_maker = CVSObjectsMaker(self.__cvs_dir)
        sha1 = objects_maker.make_object(
            None,
            self.name,
            message=self.__commit_msg
        )

    @classmethod
    def get_args(cls, parser):
        parser.add_argument(
            "-m", "--message",
            required=True,
            type=str
        )
