class RepositoryAlreadyExist(Exception):
    def __init__(self, message="Repository already exist"):
        super().__init__(message)


class RepositoryNotInitialized(Exception):
    def __init__(self, message="Repository is not initialized"):
        super().__init__(message)
