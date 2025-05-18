class ByteReader:
    @classmethod
    def get_bytes(cls, file):
        with open(file, "rb") as f:
            return f.read()