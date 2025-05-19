from master.cvs.service.PathHandler import PathHandler


class IndexFileHandler:
    def __init__(self, cvs_dir):
        path_handler = PathHandler()
        self.__index_path = path_handler.make_path(cvs_dir, "index")
        if not path_handler.exists(self.__index_path):
            open(self.__index_path, "w").close()

    def add(self, file_path, sha1):
        entries = self.read()
        entries[file_path] = sha1
        self.__write_all(entries)

    def read(self):
        path_handler = PathHandler()
        entries = {}
        if path_handler.exists(self.__index_path):
            with open(self.__index_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        path, sha1 = line.rsplit(" ", 1)
                        entries[path] = sha1
        return entries

    def __write_all(self, entries):
        with open(self.__index_path, "w") as f:
            for path, sha1 in entries.items():
                f.write(f"{path} {sha1}\n")

    def contains(self, file_path):
        entries = self.read()
        return file_path in entries

    def remove(self, file_path):
        entries = self.read()
        if file_path in entries:
            del entries[file_path]
            self.__write_all(entries)
