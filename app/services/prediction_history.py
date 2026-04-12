from sqlalchemy.orm import Session
from app.db.models import MLTask


class PredictionHistory:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def get_by_user(self, user_id: str) -> list[MLTask]:
        return (
            self.__session.query(MLTask)
            .filter(MLTask.user_id == user_id)
            .order_by(MLTask.created_at.desc())
            .all()
        )
