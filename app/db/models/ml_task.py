import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, String, ForeignKey, func, Enum as SAEnum

from app.models.enums import TaskStatus
from app.database import Base


class MLTask(Base):
    __tablename__ = "ml_tasks"

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    model_id: Mapped[str] = mapped_column(
        ForeignKey("ml_models.id"), nullable=False, index=True
    )

    input_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskStatus.PENDING,
    )

    result: Mapped[dict] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
