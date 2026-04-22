from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import app.db.models
from app.api.auth import router as auth_router
from app.api.balance import router as balance_router
from app.api.predict import router as predict_router
from app.api.prediction_history import router as history_router
from app.web.router import router as web_router
from app.database import engine, Base, get_db
from app.init_db import init_db

app = FastAPI()

app.include_router(auth_router)
app.include_router(balance_router)
app.include_router(predict_router)
app.include_router(history_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(web_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    db: Session = next(get_db())
    try:
        init_db(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
