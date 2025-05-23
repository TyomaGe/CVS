from master.cvs.service.handlers import PathHandler, HeadFileHandler
from master.cvs.service.objects import TreeMaker
from master.cvs.service.Hashier import Hashier
from master.cvs.service.ObjectWriter import ObjectWriter
from master.models.objects import Commit
from master.utilities import Time


class CommitMaker:
    def __init__(self, cvs_dir):
        self.__cvs_dir = cvs_dir
        self.__path_handler = PathHandler()
        self.__writer = ObjectWriter(cvs_dir)
        self.__tree_maker = TreeMaker(self.__cvs_dir)
        self.__head_handler = HeadFileHandler(self.__cvs_dir)

    def make_commit(self, message, author="anonymous"):
        tree_sha1 = self.__tree_maker.make_tree()
        cur_branch = self.__head_handler.get_current_branch()
        head_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "refs",
            "heads",
            cur_branch
        )
        parent_sha1 = None
        if self.__path_handler.exists(head_path):
            with open(head_path, "r") as f:
                parent_sha1 = f.read().strip()
        lines = [f"tree {tree_sha1}"]
        if parent_sha1:
            lines.append(f"parent {parent_sha1}")
        lines.append(f"author {author} {Time.get_date()}")
        lines.append(f"\n{message}")
        content = "\n".join(lines).encode("utf-8")
        sha1 = Hashier.hash(content, Commit.value)
        self.__writer.write_object(sha1, content)
        self.__path_handler.make_dirs(
            self.__path_handler.get_dirname(head_path), exist_ok=True
        )
        with open(head_path, "w") as f:
            f.write(sha1)
        print(f"\033[92mSuccessfully commited {sha1}\033[0m")
        return sha1
