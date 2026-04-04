from datetime import datetime
from abc import ABC, abstractmethod

from app.models.user import User


class Transaction(ABC):
    def __init__(
        self,
        id: str,
        amount: float,
        created_at: datetime,
        user: User,
        task_id: str | None = None,
    ):
        self.id = id
        self.amount = amount
        self.created_at = created_at
        self.user = user
        self.task_id = task_id

    @abstractmethod
    def apply(self) -> None: ...


class DebitTransaction(Transaction):
    def apply(self) -> None:
        self.user.balance.withdraw(self.amount)


class CreditTransaction(Transaction):
    def apply(self) -> None:
        self.user.balance.deposit(self.amount)

