from app.models.enums import UserRole


class User:
    def __init__(
        self,
        id: str,
        email: str,
        role: UserRole,
        password_hash: str,
        balance: float = 0.0,
    ):
        self.id = id
        self.email = email
        self.role = role
        self.__password_hash = password_hash
        self._balance = balance

    def deposit(self, amount: float) -> None:
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        else:
            self._balance -= amount

    def get_balance(self) -> float:
        return self._balance
