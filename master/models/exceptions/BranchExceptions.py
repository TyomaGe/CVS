class BranchHasNoCommits(Exception):
    def __init__(self, message="There`s no any commits in branch"):
        super().__init__(message)
