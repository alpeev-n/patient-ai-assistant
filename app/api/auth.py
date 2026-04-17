from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserResponse, UserRegister, UserLogin
from app.database import get_db
from app.services.user_service import UserService


router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    service = UserService(db)

    return service.create_user(email=user.email, password=user.password, role=user.role)


@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    db_user = service.get_user_by_email(user.email)

    if not db_user or db_user.hashed_password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return db_user
