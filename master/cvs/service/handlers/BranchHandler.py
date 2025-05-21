from master.cvs.service.handlers import PathHandler


class BranchHandler:
    def __init__(self, dir_path, cvs_dir):
        self.__path_handler = PathHandler()
        self.__dir = dir_path
        self.__cvs_dir = cvs_dir
        self.__head_path = self.__path_handler.make_path(cvs_dir,"HEAD")

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
