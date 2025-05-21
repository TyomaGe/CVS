from master.cvs.service.handlers import PathHandler
from master.models.exceptions import BranchNotExist


class BranchHandler:
    def __init__(self, dir_path, cvs_dir):
        self.__path_handler = PathHandler()
        self.__dir = dir_path
        self.__cvs_dir = cvs_dir
        self.__head_path = self.__path_handler.make_path(cvs_dir, "HEAD")

    def change_branch(self, branch):
        with open(self.__head_path, "w") as head_file:
            head_file.write(f"refs/heads/{branch}\n")

    def get_branch_list(self):
        branches = []
        branches_dir = self.__path_handler.connect_path(
            self.__cvs_dir,
            "refs",
            "heads"
        )
        for _, _, files in self.__path_handler.walk(branches_dir):
            for file in files:
                branches.append(file)
        if "master" not in branches:
            branches.append("master")
        return sorted(branches)

    def branch_exist(self, branch_name):
        branch_list = self.get_branch_list()
        if not branch_name in branch_list:
            raise BranchNotExist(f"Branch {branch_name} does not exist")

    def get_head_commit_specified_branch(self, branch_name):
        self.branch_exist(branch_name)
        branch_path = self.__path_handler.connect_path(
            self.__cvs_dir,
            "refs",
            "heads",
            branch_name
        )
        with open(branch_path, "r") as f:
            sha1 = f.read().strip()
        return sha1
