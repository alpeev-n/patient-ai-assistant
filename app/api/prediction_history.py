from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.history import MLTaskResponse, TransactionResponse
from app.services.prediction_history import PredictionHistory
from app.db.models import Transaction


router = APIRouter(prefix="/history")


@router.get("/tasks/{user_id}", response_model=list[MLTaskResponse])
def get_task_history(user_id: str, db: Session = Depends(get_db)):
    service = PredictionHistory(db)
    return service.get_by_user(user_id)


@router.get("/transactions/{user_id}", response_model=list[TransactionResponse])
def get_by_user(user_id: str, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not transactions:
        return []
    return transactions
