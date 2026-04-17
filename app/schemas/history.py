from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Any
from decimal import Decimal


class MLTaskResponse(BaseModel):
    id: str
    model_id: str
    created_at: datetime
    result: dict[str, Any] | None = None
    status: str
    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", "model_id", mode="before")
    @classmethod
    def convert_uuid_to_str(cls, v):
        return str(v)


class TransactionResponse(BaseModel):
    type: str
    task_id: str | None = None
    created_at: datetime
    amount: Decimal
    model_config = ConfigDict(from_attributes=True)

    @field_validator("type", mode="before")
    @classmethod
    def convert_enum_to_str(cls, v):
        if hasattr(v, "value"):
            return v.value
        return str(v)
