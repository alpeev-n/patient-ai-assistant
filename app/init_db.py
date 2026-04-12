from decimal import Decimal
from sqlalchemy.orm import Session

from app.db.models import MLModel
from app.services.user_service import UserService
from app.models.enums import UserRole


def init_db(session: Session) -> None:
    user_service = UserService(session)

    demo_user_email = "demo@example.com"
    try:
        user = user_service.get_user_by_email(demo_user_email)
    except ValueError:
        user = user_service.create_user(
            email=demo_user_email, password="password", role=UserRole.PATIENT
        )
        user_service.deposit(user.id, Decimal("1000.00"))

    admin_email = "admin@example.com"
    try:
        user_service.get_user_by_email(admin_email)
    except ValueError:
        user_service.create_user(
            email=admin_email, password="admin", role=UserRole.ADMIN
        )

    default_models = [
        {
            "name": "ResNet50",
            "description": "Image Classification",
            "cost": Decimal("1.00"),
        },
        {"name": "BERT", "description": "Text Classification", "cost": Decimal("0.50")},
        {"name": "YOLOv8", "description": "Object Detection", "cost": Decimal("2.00")},
    ]

    for model_data in default_models:
        exists = (
            session.query(MLModel).filter(MLModel.name == model_data["name"]).first()
        )
        if not exists:
            model = MLModel(**model_data)
            session.add(model)

    session.commit()
