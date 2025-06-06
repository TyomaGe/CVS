from master.cvs.commands import AbstractCommand
from master.cvs.service.handlers import IndexFileHandler
from master.cvs.service.handlers.FileHandler import FileHandler
from master.models.command import Reset
from master.models.exceptions import HashException


class ResetCommand(AbstractCommand):
    def __init__(self):
        self.name = Reset.name
        self.description = Reset.description
        self.__files = None
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__file_handler = FileHandler(self.__dir, self.__cvs_dir)

    def get_args(self, parser):
        parser.add_argument(
            "commit",
            type=str,
        )

    def run(self, args):
        self._check_repository_initialized()
        short_sha1 = args.commit
        full_sha1 = self.__index_handler.find_full_commit_sha1(short_sha1)
        if full_sha1 is None:
            raise HashException("Commit does not exist")
        files = self.__index_handler.get_files_from_commit(full_sha1)
        self.__file_handler.restore_files_to_directory(files, self.__dir)
        self.__index_handler.write_all(files)
        self.__index_handler.update_head(full_sha1)
        print(f"\033[93mSuccessfully rolled back to the commit"
              f" {full_sha1}\033[0m")
