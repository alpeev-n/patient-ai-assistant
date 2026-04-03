import unittest

from app.models.enums import UserRole, TaskStatus
from app.models.user import User
from app.models.ml_model import PatientAssistantModel
from app.models.task import MLTask
from app.models.prediction import PredictionResult


class TestModelIntegration(unittest.TestCase):
    def test_smoke_test_run_task(self):
        user = User(
            id="user_123",
            email="test@example.com",
            password_hash="hashed",
            role=UserRole.PATIENT,
        )

        model = PatientAssistantModel(
            id="model_1",
            name="Patient Assistant",
            description="AI assistant for patients",
            cost_per_prediction=1.0,
        )

        input_data = {"symptoms": ["headache", "fever"], "age": 30, "gender": "male"}

        task = MLTask(id="task_1", user=user, model=model, input_data=input_data)

        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertIsNone(task.result)

        try:
            result = task.run()
        except Exception as e:
            self.fail(f"task.run() raised an exception: {e}")

        self.assertEqual(task.status, TaskStatus.DONE)

        self.assertIsNotNone(task.result)

        self.assertIsInstance(result, PredictionResult)
        self.assertEqual(result.task_id, task.id)


if __name__ == "__main__":
    unittest.main()
