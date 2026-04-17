from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.predict import PredictRequest, PredictResponse
from app.database import get_db
from app.services.user_service import UserService
from app.db.models.ml_model import MLModel
from app.db.models.ml_task import MLTask
from app.models.enums import TaskStatus


router = APIRouter(prefix="/predict")


@router.post("/request", response_model=PredictResponse)
def predict_request(data: PredictRequest, db: Session = Depends(get_db)):
    service = UserService(db)

    try:
        user = service.get_user_by_id(data.user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    model = db.query(MLModel).filter(MLModel.name == data.model).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    task = MLTask(
        user_id=user.id,
        model_id=model.id,
        input_data=data.input_data,
        status=TaskStatus.DONE,
    )
    db.add(task)
    db.flush()

    service.withdraw(user_id=user.id, amount=model.cost, task_id=task.id)

    db.commit()
    db.refresh(task)

    return PredictResponse(task_id=task.id, result=task.result, status=task.status)
