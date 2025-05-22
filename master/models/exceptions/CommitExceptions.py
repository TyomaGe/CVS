class CommitNotExist(Exception):
    def __init__(self, message="Commit does not exist"):
        super().__init__(message)


class SameCommitException(Exception):
    def __init__(self, message="The same commit"):
        super().__init__(message)
