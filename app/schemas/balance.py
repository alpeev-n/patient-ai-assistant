from pydantic import BaseModel
from decimal import Decimal


class BalanceDeposit(BaseModel):
    user_id: str
    amount: Decimal


class BalanceResponse(BaseModel):
    user_id: str
    balance: Decimal
