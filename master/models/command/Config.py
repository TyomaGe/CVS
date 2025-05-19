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
