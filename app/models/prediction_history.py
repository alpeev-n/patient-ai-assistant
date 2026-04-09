from typing import List

from app.models.user import User
from app.models.ml_task import MLTask


class PredictionHistory:
    def __init__(self, user: User, tasks: list[MLTask] | None = None):
        self.user = user
        self.tasks = tasks if tasks else []

    def add_task(self, task: MLTask) -> None:
        self.tasks.append(task)

    def get_history(self) -> List[MLTask]:
        return self.tasks

    def get_last(self, n: int) -> List[MLTask]:
        if n <= 0:
            return []
        return self.tasks[-n:]
