from dataclasses import dataclass


@dataclass(frozen=True)
class Blob:
    value = "blob"
