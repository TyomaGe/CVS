class StatusPrinter:
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