import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Numeric, func, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.enums import TransactionType
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    task_id: Mapped[str | None] = mapped_column(
        ForeignKey("ml_tasks.id"), nullable=True, index=True
    )

    type: Mapped[TransactionType] = mapped_column(
        SAEnum(TransactionType, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
