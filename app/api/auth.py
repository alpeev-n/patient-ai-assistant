from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas.user import UserResponse, UserRegister, UserLogin
from app.database import get_db
from app.services.user_service import UserService
from app.jwt import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    service = UserService(db)

    return service.create_user(email=user.email, password=user.password, role=user.role)


@router.post("/login")
def login(response: Response, user_data: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)

    try:
        user = service.get_user_by_email(user_data.email)
    except ValueError:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds()),
        path="/",
    )

    return {"message": "Login successful", "user_id": user.id}
