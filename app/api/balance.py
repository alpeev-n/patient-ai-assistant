from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.balance import BalanceDeposit, BalanceResponse
from app.database import get_db
from app.services.user_service import UserService


router = APIRouter(prefix="/balance")


@router.get("/{user_id}", response_model=BalanceResponse)
def get_balance(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)

    try:
        user = service.get_user_by_id(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return BalanceResponse(user_id=user.id, balance=user.balance)


@router.post("/deposit", response_model=BalanceResponse)
def deposit(data: BalanceDeposit, db: Session = Depends(get_db)):
    service = UserService(db)

    try:
        service.deposit(data.user_id, data.amount)
        user = service.get_user_by_id(data.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return BalanceResponse(user_id=user.id, balance=user.balance)
