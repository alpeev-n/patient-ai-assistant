from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from sqlalchemy.orm import Session
import app.db.models
from app.database import engine, Base, get_db
from app.init_db import init_db

app = FastAPI()


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
