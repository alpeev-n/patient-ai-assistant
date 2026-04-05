class Balance:
    def __init__(self, amount: float = 0.0):
        self._amount = amount

    def deposit(self, amount: float) -> None:
        self._amount += amount

    def withdraw(self, amount: float) -> None:
        if amount > self._amount:
            raise ValueError("Insufficient balance")
        self._amount -= amount

    @property
    def amount(self) -> float:
        return self._amount
