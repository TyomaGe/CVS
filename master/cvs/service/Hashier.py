import hashlib


class Hashier:
    @classmethod
    def hash(cls, data, obj_type):
        header = f"{obj_type} {len(data)}\0".encode("utf-8")
        full_data = header + data
        sha1 = hashlib.sha1(full_data).hexdigest()
        return sha1

    @classmethod
    def get_hash_parts(cls, sha1):
        return sha1[:2], sha1[2:]
