from decimal import Decimal
from pydantic import BaseModel, Field


class BalanceDeposit(BaseModel):
    user_id: str
    amount: Decimal = Field(gt=0)


class BalanceResponse(BaseModel):
    user_id: str
    balance: Decimal
