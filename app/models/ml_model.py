from abc import ABC, abstractmethod


class MLModel(ABC):
    def __init__(
        self, id: str, name: str, description: str, cost_per_prediction: float
    ):
        self.id = id
        self.name = name
        self.description = description
        self.cost_per_prediction = cost_per_prediction

    @abstractmethod
    def predict(self, input_data: dict) -> dict: ...


class PatientAssistantModel(MLModel):
    def predict(self, input_data: dict) -> dict:
        return {
            "psychological_support": None,
            "diagnosis_summary": None,
            "doctor_questions": None,
            "examination_plan": None,
            "evidence_based_recommendations": None,
        }
