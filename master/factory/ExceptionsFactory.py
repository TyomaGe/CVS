from master.models.exceptions import *


class ExceptionsFactory:
    @classmethod
    def get_exceptions(cls):
        return (
            RepositoryAlreadyExist,
            RepositoryNotInitialized,
            EmptyIndexException,
            UnchangedIndexException
        )
