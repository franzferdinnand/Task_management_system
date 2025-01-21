from enum import IntEnum


class Status(IntEnum):
    NEW = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

HELP_TEXT_PRIORITIES = "1: LOW, 2: MEDIUM, 3: HIGH"
HELP_TEXT_STATUSES = "1: NEW, 2: IN_PROGRESS, 3: COMPLETED"