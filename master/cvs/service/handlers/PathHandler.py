import os
import ctypes


class PathHandler:
    @staticmethod
    def make_path(path, file):
        return os.path.join(path, file)

    @staticmethod
    def connect_path(*parts):
        return os.path.join(*parts)

    @staticmethod
    def get_dirname(path):
        return os.path.dirname(path)

    @staticmethod
    def getcwd():
        return os.getcwd()

    @staticmethod
    def walk(path):
        return os.walk(path)

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)

    @staticmethod
    def make_dirs(path, exist_ok=False):
        os.makedirs(path, exist_ok=exist_ok)

    @staticmethod
    def get_rel_path(path, start):
        return os.path.relpath(path, start)

    @staticmethod
    def is_windows():
        return os.name == 'nt'

    @classmethod
    def set_hidden(cls, path):
        if cls.is_windows():
            attr_hidden = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(path, attr_hidden)

    @classmethod
    def remove_file(cls, path):
        if cls.exists(path) and cls.is_file(path):
            os.remove(path)

    @staticmethod
    def remove_empty_dirs_recursive(root_path):
        for root, dirs, _ in os.walk(root_path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    os.rmdir(dir_path)
                except OSError:
                    pass
        try:
            os.rmdir(root_path)
        except OSError:
            pass
