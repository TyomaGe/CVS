from master.cvs.service.handlers import IndexFileHandler
from master.cvs.service.objects import TreeMaker, BlobMaker, CommitMaker
from master.models.objects import Blob, Tree, Commit


class CVSObjectsMaker:
    def __init__(self, cvs_dir):
        self.cvs_dir = cvs_dir

    def make_object(self, file_path, obj_type, **kwargs):
        if obj_type == Blob.value:
            return self.__make_blob_object(file_path)
        elif obj_type == Tree.value:
            return self.__make_tree_object()
        elif obj_type == Commit.value:
            return self.__make_commit_object(kwargs.get("message"))
        return None

    def __make_blob_object(self, file_path):
        blob_maker = BlobMaker(self.cvs_dir)
        return blob_maker.make_blob(file_path)

    def __make_tree_object(self):
        index_handler = IndexFileHandler(self.cvs_dir)
        tree_maker = TreeMaker(index_handler, self.cvs_dir)
        return tree_maker.make_tree()

    def __make_commit_object(self, message):
        commit_maker = CommitMaker(self.cvs_dir)
        return commit_maker.make_commit(message)
