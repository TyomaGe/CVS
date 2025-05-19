from master.cvs.service.ByteReader import ByteReader
from master.cvs.service.Hashier import Hashier
from master.cvs.service.PathHandler import PathHandler
from master.models.objects import Blob


class CVSObjectsMaker:
    def __init__(self, obj_type, cvs_dir):
        self.__obj_type = obj_type
        self.__cvs_dir = cvs_dir

    def make_object(self, file_path):
        sha1 = None
        if self.__obj_type == Blob.value:
            sha1 = self.__make_blob_file(file_path)
        return sha1

    def __make_blob_file(self, file_path):
        data = ByteReader.get_bytes(file_path)
        sha1 = Hashier.hash(data, self.__obj_type)
        path_handler = PathHandler()
        folder = sha1[:2]
        filename = sha1[2:]
        obj_dir = path_handler.connect_path(self.__cvs_dir, "objects", folder)
        object_path = path_handler.make_path(obj_dir, filename)
        path_handler.make_dirs(obj_dir, exist_ok=True)
        if not path_handler.exists(object_path):
            with open(object_path, "wb") as f:
                f.write(data)
        return sha1
