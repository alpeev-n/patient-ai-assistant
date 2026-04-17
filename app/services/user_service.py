from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.enums import TransactionType
from app.db.models import User
from app.db.models import Transaction


class UserService:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create_user(self, email: str, password: str, role: str) -> User:
        user = User(email=email, hashed_password=password, role=role)
        self.__session.add(user)
        self.__session.commit()
        self.__session.refresh(user)
        return user

    def get_user_by_id(self, id: str) -> User:
        user = self.__session.query(User).filter(User.id == id).first()
        if not user:
            raise ValueError(f"User with id {id} not found")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.__session.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError(f"User with email {email} not found")
        return user

    def deposit(self, user_id: str, amount: Decimal) -> None:
        user = self.get_user_by_id(user_id)
        user.balance += amount
        transaction = Transaction(
            user_id=user.id, type=TransactionType.CREDIT, amount=amount
        )
        self.__session.add(transaction)
        self.__session.commit()

    def withdraw(
        self, user_id: str, amount: Decimal, task_id: str | None = None
    ) -> None:
        user = self.get_user_by_id(user_id)

        if user.balance < amount:
            raise ValueError("Insufficient funds")

        user.balance -= amount

        transaction = Transaction(
            user_id=user.id, type=TransactionType.DEBIT, amount=amount, task_id=task_id
        )
        self.__session.add(transaction)
        self.__session.commit()
