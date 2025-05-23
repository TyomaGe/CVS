class BranchHasNoCommits(Exception):
    def __init__(self, message="There`s no any commits in branch"):
        super().__init__(message)


class BranchNotExist(Exception):
    def __init__(self, message="Branch does not exist"):
        super().__init__(message)


class CurrentBranchException(Exception):
    def __init__(self, message="Something wrong with current branch"):
        super().__init__(message)


class MasterBranchException(Exception):
    def __init__(self, message="Something wrong with master branch"):
        super().__init__(message)


class MergeException(Exception):
    def __init__(self, message="Merge exception"):
        super().__init__(message)


class MergeConflictException(Exception):
    def __init__(self, message="Merge conflict exception"):
        super().__init__(message)
