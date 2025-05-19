import os
import ctypes


class PathHandler:
    @classmethod
    def make_path(cls, path, file):
        return os.path.join(path, file)

    @classmethod
    def connect_path(cls, *parts):
        return os.path.join(*parts)

    @classmethod
    def getcwd(cls):
        return os.getcwd()

    @classmethod
    def walk(cls, path):
        return os.walk(path)

    @classmethod
    def exists(cls, path):
        return os.path.exists(path)

    @classmethod
    def is_file(cls, path):
        return os.path.isfile(path)

    @classmethod
    def is_dir(cls, path):
        return os.path.isdir(path)

    @classmethod
    def make_dirs(cls, path, exist_ok=False):
        os.makedirs(path, exist_ok=exist_ok)

    @classmethod
    def get_rel_path(cls, path, start):
        return os.path.relpath(path, start)

    @classmethod
    def is_windows(cls):
        return os.name == 'nt'

    @classmethod
    def set_hidden(cls, path):
        if cls.is_windows():
            attr_hidden = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(path, attr_hidden)
