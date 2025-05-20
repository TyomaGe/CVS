from dataclasses import dataclass


@dataclass(frozen=True)
class Init:
    name = "init"
    description = ("Initialize a new CVS repository"
                   " in the current directory")


@dataclass(frozen=True)
class Add:
    name = "add"
    description = ("Add files or directories to the staging area"
                   " for the next commit")


@dataclass(frozen=True)
class Commit:
    name = "commit"
    description = "Create a new commit from the staged changes"


@dataclass(frozen=True)
class Status:
    name = "status"
    description = ("Show the current state of the working directory"
                   " and staging area")


@dataclass(frozen=True)
class Log:
    name = "log"
    description = "Display the commit history of the current branch"


@dataclass(frozen=True)
class Reset:
    name = "reset"
    description = "Reset working directory and index to the specified commit"


@dataclass(frozen=True)
class Rm:
    name = "rm"
    description = ("Remove files or directories from"
                   " the index and working directory")
