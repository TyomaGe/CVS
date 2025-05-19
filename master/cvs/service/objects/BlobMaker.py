from master.cvs.service.ByteReader import ByteReader
from master.cvs.service.Hashier import Hashier
from master.models.objects import Blob
from master.cvs.service.ObjectWriter import ObjectWriter


class BlobMaker:
    def __init__(self, cvs_dir):
        self.__cvs_dir = cvs_dir
        self.__writer = ObjectWriter(cvs_dir)

    def make_blob(self, file_path):
        data = ByteReader.get_bytes(file_path)
        sha1 = Hashier.hash(data, Blob.value)
        self.__writer.write_object(sha1, data)
        return sha1
