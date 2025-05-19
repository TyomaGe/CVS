from dataclasses import dataclass


@dataclass(frozen=True)
class Init:
    name = "init"
    description = ""


@dataclass(frozen=True)
class Add:
    name = "add"
    description = ""


@dataclass(frozen=True)
class Commit:
    name = "commit"
    description = ""


@dataclass(frozen=True)
class Status:
    name = "status"
    description = ""


@dataclass(frozen=True)
class Log:
    name = "log"
    description = ""
