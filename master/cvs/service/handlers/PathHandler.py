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
    def get_dirname(cls, path):
        return os.path.dirname(path)

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

    @classmethod
    def remove_file(cls, path):
        if cls.exists(path) and cls.is_file(path):
            os.remove(path)

    @classmethod
    def remove_empty_dirs_recursive(cls, root_path):
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
