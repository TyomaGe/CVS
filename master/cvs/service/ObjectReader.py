from master.cvs.service import Hashier
from master.cvs.service.handlers import PathHandler


class ObjectReader:
    def __init__(self, cvs_dir):
        self.__cvs_dir = cvs_dir
        self.__path_handler = PathHandler()

    def read_object(self, sha1):
        folder, filename = Hashier.get_hash_parts(sha1)
        obj_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "objects",
            folder,
            filename
        )
        with open(obj_path, "rb") as f:
            return f.read()
