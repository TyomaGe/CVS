import os

class PathMaker:
    @classmethod
    def make_path(cls, path, file):
        return os.path.join(path, file)

    @classmethod
    def connect_path(cls, *parts):
        return os.path.join(*parts)
