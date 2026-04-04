from app.models.balance import Balance
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
        self.balance = Balance(balance)

