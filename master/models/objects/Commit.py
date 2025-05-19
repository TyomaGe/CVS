from dataclasses import dataclass


@dataclass(frozen=True)
class Commit:
    value = "commit"
