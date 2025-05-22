import difflib

from master.cvs.commands import AbstractCommand
from master.cvs.service import ByteReader, Printer
from master.cvs.service.ObjectReader import ObjectReader
from master.cvs.service.handlers import *
from master.models.command import Diff
from master.models.exceptions import CommitNotExist, SameCommitException


class DiffCommand(AbstractCommand):
    def __init__(self):
        self.name = Diff.name
        self.description = Diff.description
        self.__dir, self.__cvs_dir = self._get_dirs_paths()
        self.__index_handler = IndexFileHandler(self.__cvs_dir)
        self.__byte_reader = ByteReader()
        self.__object_reader = ObjectReader(self.__cvs_dir)
        self.__printer = Printer()

    def get_args(self, parser):
        parser.add_argument(
            "commits",
            nargs=2,
        )

    def run(self, args):
        self._check_repository_initialized()
        first_hash, second_hash = args.commits
        first_files, second_files = self.__get_files_from_commits(
            first_hash,
            second_hash
        )
        first_paths = set(first_files.keys())
        second_paths = set(second_files.keys())
        for path in sorted(first_paths & second_paths):
            first_sha1 = first_files[path]
            second_sha1 = second_files[path]
            if first_sha1 == second_sha1:
                continue
            first_content, second_content = self.__get_decoded_blobs_content(
                first_sha1,
                second_sha1
            )
            diff_file = difflib.unified_diff(
                first_content,
                second_content,
                fromfile=f".\\{path}",
                tofile=f".\\{path}"
            )
            self.__printer.print_diff_file(diff_file)
        self.__printer.print_added_files(first_paths, second_paths)
        self.__printer.print_deleted_files(first_paths, second_paths)

    def __get_files_from_commits(self, first_hash, second_hash):
        full_first = self.__index_handler.find_full_commit_sha1(first_hash)
        if not full_first:
            raise CommitNotExist("The first commit is specified incorrectly")
        full_second = self.__index_handler.find_full_commit_sha1(second_hash)
        if not full_second:
            raise CommitNotExist("The second commit is specified incorrectly")
        if full_first == full_second:
            raise SameCommitException("Commits are identical")
        first_files = self.__index_handler.get_files_from_commit(full_first)
        second_files = self.__index_handler.get_files_from_commit(full_second)
        return first_files, second_files

    def __get_decoded_blobs_content(self, first_sha1, second_sha1):
        first_blob = self.__object_reader.read_object(first_sha1)
        second_blob = self.__object_reader.read_object(second_sha1)
        first_decoded = first_blob.decode(errors="ignore").splitlines()
        second_decoded = second_blob.decode(errors="ignore").splitlines()
        return first_decoded, second_decoded
