import os

from master.cvs.service import Hashier
from master.cvs.service.handlers import IndexFileHandler, PathHandler


class FileHandler:
    def __init__(self, dir_path, cvs_dir):
        self.__idx_handler = IndexFileHandler(cvs_dir)
        self.__dir = dir_path
        self.__cvs_dir = cvs_dir
        self.__path_handler = PathHandler()

    def restore_files_to_directory(self, files_dict, root_dir):
        current_index = self.__idx_handler.read()
        for rel_path in current_index:
            abs_path = self.__path_handler.connect_path(root_dir, rel_path)
            if self.__path_handler.exists(abs_path):
                self.__path_handler.remove_file(abs_path)
            self.__path_handler.remove_empty_dirs_recursive(root_dir)
        for rel_path, sha1 in files_dict.items():
            folder, filename = Hashier.get_hash_parts(sha1)
            object_path = self.__path_handler.connect_path(
                self.__cvs_dir, "objects", folder, filename
            )
            if not self.__path_handler.exists(object_path):
                continue
            with open(object_path, "rb") as f:
                content = f.read()
            target_path = self.__path_handler.connect_path(root_dir, rel_path)
            target_dir = self.__path_handler.get_dirname(target_path)
            if not self.__path_handler.exists(target_dir):
                self.__path_handler.make_dirs(target_dir, exist_ok=True)
            with open(target_path, "wb") as out_file:
                out_file.write(content)

    @classmethod
    def remove_from_index(cls, relative_path, idx_handler, tracked_files):
        matched = False
        for tracked_path in tracked_files:
            if (tracked_path == relative_path or
                    tracked_path.startswith(relative_path + os.sep)):
                matched = True
                idx_handler.restore([tracked_path])
        if not matched:
            print(f"\033[91m'{relative_path}' is not tracked\033[0m")

    def remove_dir(self, index_handler, abs_dir_path):
        for root, _, files in self.__path_handler.walk(abs_dir_path):
            for f in files:
                full_path = self.__path_handler.make_path(root, f)
                rel_path = self.__path_handler.get_rel_path(
                    full_path,
                    self.__dir
                )
                self.__remove_if_tracked(index_handler, rel_path, full_path)
        self.__path_handler.remove_empty_dirs_recursive(abs_dir_path)

    def remove_file(self, index_handler, relative_path, abs_path):
        self.__remove_if_tracked(index_handler, relative_path, abs_path)
        self.__path_handler.remove_empty_dirs_recursive(
            self.__path_handler.get_dirname(abs_path)
        )

    def handle_nonexistent_path(self, rel_path, idx_handler, tracked_files):
        matched = False
        for tracked_path in tracked_files:
            if (tracked_path == rel_path or
                    tracked_path.startswith(rel_path + os.sep)):
                matched = True
                self.__remove_if_tracked(idx_handler, tracked_path, None)
        if not matched:
            print(f"\033[91m'{rel_path}' is not tracked\033[0m")

    def __remove_if_tracked(self, index_handler, rel_path, abs_path):
        if index_handler.contains(rel_path):
            if abs_path and self.__path_handler.exists(abs_path):
                self.__path_handler.remove_file(abs_path)
            index_handler.remove(rel_path)
        else:
            print(f"\033[91m'{rel_path}' is not tracked\033[0m")
