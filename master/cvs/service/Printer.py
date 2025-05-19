class Printer:
    @classmethod
    def __print_staged_changes(cls, staged_changes):
        if staged_changes:
            print("Changes to be committed:")
            for file in staged_changes.get("modified", []):
                print(f"\033[32m\tmodified:   {file}\033[0m")
            for file in staged_changes.get("new file", []):
                print(f"\033[32m\tnew file:   {file}\033[0m")
            print()

    @classmethod
    def __print_unstaged_changes(cls, unstaged_changes):
        if unstaged_changes.get("modified") or unstaged_changes.get("deleted"):
            print("Changes not staged for commit:")
            for file in unstaged_changes.get("modified", []):
                print(f"\033[31m\tmodified:   {file}\033[0m")
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
