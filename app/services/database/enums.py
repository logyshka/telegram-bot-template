from strenum import StrEnum
from enum import auto


class UserRole(StrEnum):
    OWNER = auto()
    ADMIN = auto()
    USER = auto()


class SearchSection(StrEnum):
    USER = auto()


__all__ = (
    "UserRole",
    "SearchSection",
)
