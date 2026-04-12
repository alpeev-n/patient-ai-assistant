import uuid
from datetime import datetime
from typing import Optional

from app.models.enums import TaskStatus
from app.models.user import User
from app.models.ml_model import MLModel
from app.models.prediction import PredictionResult


class MLTask:
    def __init__(
        self,
        id: str,
        user: User,
        model: MLModel,
        input_data: dict,
        status: TaskStatus = TaskStatus.PENDING,
        result: Optional[PredictionResult] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.user = user
        self.model = model
        self.input_data = input_data
        self.status = status
        self.result = result
        self.created_at = created_at or datetime.now()

    def run(self) -> "PredictionResult":
        self.status = TaskStatus.RUNNING

        try:
            model_output = self.model.predict(self.input_data)

            result_id = str(uuid.uuid4())

            prediction_result = PredictionResult(
                id=result_id,
                task_id=self.id,
                psychological_support=model_output.get("psychological_support"),
                diagnosis_summary=model_output.get("diagnosis_summary"),
                doctor_questions=model_output.get("doctor_questions"),
                examination_plan=model_output.get("examination_plan"),
                evidence_based_recommendations=model_output.get(
                    "evidence_based_recommendations"
                ),
                created_at=datetime.now(),
            )

            self.result = prediction_result

            self.status = TaskStatus.DONE

        except Exception:
            self.status = TaskStatus.FAILED
            raise

        return self.result
