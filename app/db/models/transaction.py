import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, ForeignKey, Numeric, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

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
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    task_id: Mapped[str | None] = mapped_column(
        ForeignKey("ml_tasks.id"),
        nullable=True,
        index=True
    )

    type: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint("type IN ('debit', 'credit')", name="check_transaction_type"),
    )
