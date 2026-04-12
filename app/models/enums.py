from enum import Enum


class UserRole(Enum):
    PATIENT = "patient"
    ADMIN = "admin"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class TransactionType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"
