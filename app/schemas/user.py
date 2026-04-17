from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from datetime import datetime

from app.models.enums import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
