from pydantic import BaseModel
from typing import Any


class PredictRequest(BaseModel):
    user_id: str
    input_data: dict[str, Any]
    model: str


class PredictResponse(BaseModel):
    task_id: str
    result: dict[str, Any] | None = None
    status: str
