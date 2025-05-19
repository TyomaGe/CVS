class EmptyIndexException(Exception):
    def __init__(self, message="Index is empty"):
        super().__init__(message)


class UnchangedIndexException(Exception):
    def __init__(self, message="Index matches it`s last version"):
        super().__init__(message)
