from master.cvs.service.handlers.PathHandler import PathHandler
from master.models.exceptions import BranchHasNoCommits


class HeadFileHandler:
    def __init__(self, cvs_dir):
        self.__cvs_dir = cvs_dir
        self.__path_handler = PathHandler()
        self.__head_path = self.__path_handler.connect_path(cvs_dir, "HEAD")

    def change_branch(self, branch):
        with open(self.__head_path, "w") as head_file:
            head_file.write(f"refs/heads/{branch}\n")

    def get_current_branch(self):
        with open(self.__head_path, "r") as f:
            ref = f.read().strip()
            return ref[len("refs/heads/"):]

    def get_head_commit(self):
        with open(self.__head_path, "r") as f:
            branch_ref = f.read().strip()
        branch_path = self.__path_handler.connect_path(
            self.__path_handler.get_dirname(self.__head_path),
            branch_ref
        )
        try:
            with open(branch_path, "r") as f:
                return f.read().strip()
        except FileNotFoundError as e:
            raise BranchHasNoCommits(f"There`s no commits yet in branch"
                                     f" '{branch_ref[len("refs/heads/"):]}'"
            ) from e
