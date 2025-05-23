from master.models.text import MERGE_SUCCESS_TEXT


class Printer:
    @classmethod
    def __print_staged_changes(cls, staged_changes):
        if staged_changes:
            print("Changes to be committed:")
            for file in staged_changes.get("modified", []):
                print(f"\033[32m\tmodified:   {file}\033[0m")
            for file in staged_changes.get("new file", []):
                print(f"\033[32m\tnew file:   {file}\033[0m")
            for file in staged_changes.get("deleted", []):
                print(f"\033[32m\tdeleted:    {file}\033[0m")
            print()

    @classmethod
    def __print_unstaged_changes(cls, unstaged_changes):
        if unstaged_changes.get("modified") or unstaged_changes.get("deleted"):
            print("Changes not staged for commit:")
            for file in unstaged_changes.get("modified", []):
                print(f"\033[31m\tmodified:   {file}\033[0m")
            for file in unstaged_changes.get("deleted", []):
                print(f"\033[31m\tdeleted:    {file}\033[0m")
            print()

    def print_status(self, branch, staged_changes, unstaged_changes):
        print(f"On branch {branch}\n")
        self.__print_staged_changes(staged_changes)
        self.__print_unstaged_changes(unstaged_changes)

    @classmethod
    def print_commit(cls, sha1, commit_data, current_branch, head_commit):
        branch_info = ("\033[0m (\033[36mHEAD\033[0m -> \033[32m{}\033[0m)"
                       .format(current_branch)) if sha1 == head_commit else ""
        print("\033[33mcommit {}{}\033[0m".format(sha1, branch_info))
        print("Author: {}".format(commit_data['author']))
        print("Date:   {}\n".format(commit_data['date']))
        print("    {}\n".format(commit_data['message']))

    @classmethod
    def print_branch_list(cls, branches, cur_branch):
        for branch in branches:
            if branch == cur_branch:
                print(f"\033[32m* {cur_branch}\033[0m")
            else:
                print(f"  {branch}")

    @classmethod
    def print_diff_file(cls, diff_file):
        for line in diff_file:
            if line.startswith('+') and not line.startswith('+++'):
                print(f"\033[32m{line}\033[0m")
            elif line.startswith('-') and not line.startswith('---'):
                print(f"\033[31m{line}\033[0m")
            else:
                print(line)
        print()

    @classmethod
    def print_deleted_files(cls, first_paths, second_paths):
        for path in sorted(first_paths - second_paths):
            print(f"\033[31mFile deleted: {path}\033[0m")

    @classmethod
    def print_added_files(cls, first_paths, second_paths):
        for path in sorted(second_paths - first_paths):
            print(f"\033[32mFile added: {path}\033[0m")

    @classmethod
    def print_merge_success(
            cls,
            merge_branch,
            target_branch,
            new_files_count,
            resolved_conflicts
    ):
        print(MERGE_SUCCESS_TEXT.format(
                merge_branch=merge_branch,
                target_branch=target_branch,
                new_files_count=new_files_count,
                resolved_conflicts=resolved_conflicts
            )
        )