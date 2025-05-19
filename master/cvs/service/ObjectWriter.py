from master.cvs.service.Hashier import Hashier
from master.cvs.service.handlers import PathHandler


class ObjectWriter:
    def __init__(self, cvs_dir):
        self.__cvs_dir = cvs_dir
        self.__path_handler = PathHandler()

    def write_object(self, sha1, content):
        folder, filename = Hashier.get_hash_parts(sha1)
        obj_dir = self.__path_handler.connect_path(
            self.__cvs_dir,
            "objects",
            folder
        )
        object_path = self.__path_handler.make_path(obj_dir, filename)
        self.__path_handler.make_dirs(obj_dir, exist_ok=True)
        if not self.__path_handler.exists(object_path):
            with open(object_path, "wb") as f:
                f.write(content)
