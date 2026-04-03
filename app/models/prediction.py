from datetime import datetime


class PredictionResult:
    def __init__(
        self,
        id: str,
        task_id: str,
        psychological_support: str | None,
        diagnosis_summary: str | None,
        doctor_questions: list[str] | None,
        examination_plan: dict | None,
        evidence_based_recommendations: list[dict] | None,
        created_at: datetime,
    ):
        self.id = id
        self.task_id = task_id
        self.psychological_support = psychological_support
        self.diagnosis_summary = diagnosis_summary
        self.doctor_questions = doctor_questions
        self.examination_plan = examination_plan
        self.evidence_based_recommendations = evidence_based_recommendations
        self.created_at = created_at
