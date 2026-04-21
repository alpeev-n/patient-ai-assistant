from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.db.models.ml_model import MLModel
from app.db.models.ml_task import MLTask
from app.db.models.transaction import Transaction
from app.db.models.user import User
from app.jwt import create_access_token, decode_access_token, verify_password
from app.models.enums import TaskStatus, UserRole
from app.publisher import publish_ml_task
from app.services.user_service import UserService

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter()


def get_optional_user(request: Request, db: Session) -> Optional[User]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def render(template: str, request: Request, context: dict) -> HTMLResponse:
    return templates.TemplateResponse(request, template, context)


# ── Public pages ──────────────────────────────────────────────────────────────


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user = get_optional_user(request, db)
    return render("index.html", request, {"user": user})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if get_optional_user(request, db):
        return RedirectResponse("/dashboard", status_code=302)
    return render("login.html", request, {"user": None})


@router.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    service = UserService(db)
    try:
        user = service.get_user_by_email(email)
    except ValueError:
        return render(
            "login.html",
            request,
            {"user": None, "error": "Неверный email или пароль", "email": email},
        )

    if not verify_password(password, user.hashed_password):
        return render(
            "login.html",
            request,
            {"user": None, "error": "Неверный email или пароль", "email": email},
        )

    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(
        key="access_token", value=token, httponly=True, samesite="lax", path="/"
    )
    return response


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    if get_optional_user(request, db):
        return RedirectResponse("/dashboard", status_code=302)
    return render("register.html", request, {"user": None})


@router.post("/register", response_class=HTMLResponse)
def register_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    if password != password2:
        return render(
            "register.html",
            request,
            {"user": None, "error": "Пароли не совпадают", "email": email},
        )

    if len(password) < 8:
        return render(
            "register.html",
            request,
            {
                "user": None,
                "error": "Пароль должен быть не менее 8 символов",
                "email": email,
            },
        )

    service = UserService(db)
    try:
        user = service.create_user(
            email=email, password=password, role=UserRole.PATIENT
        )
    except Exception:
        return render(
            "register.html",
            request,
            {
                "user": None,
                "error": "Пользователь с таким email уже существует",
                "email": email,
            },
        )

    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(
        key="access_token", value=token, httponly=True, samesite="lax", path="/"
    )
    return response


@router.get("/logout")
def logout() -> RedirectResponse:
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token", path="/")
    return response


# ── Protected pages ───────────────────────────────────────────────────────────


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)
    db.refresh(user)
    return render("dashboard.html", request, {"user": user})


@router.post("/dashboard/deposit", response_class=HTMLResponse)
def deposit(
    request: Request,
    amount: float = Form(...),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)

    if amount <= 0:
        db.refresh(user)
        return render(
            "dashboard.html",
            request,
            {"user": user, "error": "Сумма должна быть больше нуля"},
        )

    service = UserService(db)
    service.deposit(user.id, Decimal(str(amount)))
    db.refresh(user)
    return render(
        "dashboard.html",
        request,
        {"user": user, "success": f"Баланс пополнен на {amount:.2f} кредитов"},
    )


@router.get("/predict", response_class=HTMLResponse)
def predict_page(
    request: Request, db: Session = Depends(get_db), task_id: Optional[str] = None
) -> HTMLResponse:
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)

    model = db.query(MLModel).first()
    db.refresh(user)

    task = None
    if task_id:
        task = (
            db.query(MLTask)
            .filter(MLTask.id == task_id, MLTask.user_id == user.id)
            .first()
        )

    return render(
        "predict.html",
        request,
        {"user": user, "cost": model.cost if model else "—", "task": task},
    )


@router.post("/predict/submit", response_class=HTMLResponse)
def predict_submit(
    request: Request,
    symptoms: str = Form(...),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)

    db.refresh(user)
    model = db.query(MLModel).first()

    if not model:
        return render(
            "predict.html",
            request,
            {"user": user, "cost": "—", "error": "ML-модель не найдена"},
        )

    if user.balance < model.cost:
        return render(
            "predict.html",
            request,
            {
                "user": user,
                "cost": model.cost,
                "error": f"Недостаточно средств. Нужно {model.cost} кр., доступно {user.balance:.2f} кр.",
            },
        )

    task = MLTask(
        user_id=user.id,
        model_id=model.id,
        input_data={"symptoms": symptoms},
        status=TaskStatus.PENDING,
    )
    db.add(task)
    db.flush()

    service = UserService(db)
    try:
        service.withdraw(user_id=user.id, amount=model.cost, task_id=task.id)
    except ValueError as e:
        db.rollback()
        return render(
            "predict.html", request, {"user": user, "cost": model.cost, "error": str(e)}
        )

    db.commit()
    db.refresh(task)

    publish_ml_task(
        {
            "task_id": task.id,
            "features": {"symptoms": symptoms},
            "model": model.name,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    return RedirectResponse(f"/predict?task_id={task.id}", status_code=302)


@router.get("/history", response_class=HTMLResponse)
def history(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=302)

    tasks = (
        db.query(MLTask)
        .filter(MLTask.user_id == user.id)
        .order_by(MLTask.created_at.desc())
        .all()
    )
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.created_at.desc())
        .all()
    )

    return render(
        "history.html",
        request,
        {"user": user, "tasks": tasks, "transactions": transactions},
    )
