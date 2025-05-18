class HeadFileHandler:
    def __init__(self, path):
        self.__path = path

    def change_branch(self, branch):
        with open(self.__path, "w") as head_file:
            head_file.write(f"refs/heads/{branch}\n")