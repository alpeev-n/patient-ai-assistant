from dotenv import load_dotenv

load_dotenv()
import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.services.user_service import UserService
from app.services.prediction_history import PredictionHistory


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    yield db
    db.close()


def test_create_user(session):
    service = UserService(session)
    user = service.create_user(email="test@example.com", password="secret", role="user")

    assert user.email == "test@example.com"
    assert user.role == "user"
    assert user.id is not None


def test_deposit_and_withdraw(session):
    service = UserService(session)
    user = service.create_user(email="test@example.com", password="secret", role="user")

    service.deposit(user.id, Decimal("100.00"))
    assert user.balance == Decimal("100.00")

    # Withdraw
    service.withdraw(user.id, Decimal("30.00"))
    assert user.balance == Decimal("70.00")


def test_insufficient_funds(session):
    service = UserService(session)
    user = service.create_user(email="test@example.com", password="secret", role="user")

    with pytest.raises(ValueError, match="Insufficient funds"):
        service.withdraw(user.id, Decimal("10.00"))


def test_prediction_history(session):
    from app.db.models import MLTask, MLModel

    user_service = UserService(session)
    user = user_service.create_user(
        email="test@example.com", password="secret", role="user"
    )

    model = MLModel(name="TestModel", description="Test", cost=Decimal("1.00"))
    session.add(model)
    session.commit()

    task1 = MLTask(
        user_id=user.id, model_id=model.id, status="completed", input_data="{}"
    )
    task2 = MLTask(user_id=user.id, model_id=model.id, status="failed", input_data="{}")
    session.add_all([task1, task2])
    session.commit()

    history_service = PredictionHistory(session)
    tasks = history_service.get_by_user(user.id)

    assert len(tasks) == 2
    assert tasks[0].id in [task1.id, task2.id]
