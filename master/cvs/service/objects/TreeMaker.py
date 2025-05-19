import os
from collections import defaultdict
from master.cvs.service.Hashier import Hashier
from master.models.objects import Tree
from master.cvs.service.ObjectWriter import ObjectWriter


class TreeMaker:
    def __init__(self, index_handler, cvs_dir):
        self.__index_handler = index_handler
        self.__cvs_dir = cvs_dir
        self.__writer = ObjectWriter(cvs_dir)

    def make_tree(self):
        entries = self.__index_handler.read()
        return self.__build_tree(entries)

    def __build_tree(self, entries):
        tree_structure = defaultdict(list)
        for rel_path, sha1 in entries.items():
            parts = rel_path.split(os.sep)
            if len(parts) == 1:
                tree_structure["."].append((rel_path, sha1))
            else:
                dir_path = parts[0]
                tree_structure[dir_path].append((os.sep.join(parts[1:]), sha1))
        tree_entries = []
        for path, sha1 in tree_structure["."]:
            tree_entries.append(f"100644 {sha1} {path}")
        for dir_name, children in tree_structure.items():
            if dir_name == ".":
                continue
            sub_index = {path: sha1 for path, sha1 in children}
            sub_tree_sha1 = self.__build_tree(sub_index)
            tree_entries.append(f"040000 {sub_tree_sha1} {dir_name}")
        tree_content = "\n".join(tree_entries).encode("utf-8")
        sha1 = Hashier.hash(tree_content, Tree.value)
        self.__writer.write_object(sha1, tree_content)
        return sha1
