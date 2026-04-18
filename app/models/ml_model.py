from openai import OpenAI
import os
import json
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = OpenAI(
            api_key=os.getenv("QWEN_API_KEY"),
            base_url=os.getenv("QWEN_BASE_URL")
        )

    def predict(self, input_data: dict) -> dict:
        symptoms = input_data.get("symptoms", "") or input_data.get("text", "")

        if not symptoms:
            return {
                "psychological_support": "No symptoms provided.",
                "diagnosis_summary": "Insufficient data for analysis.",
                "doctor_questions": [],
                "examination_plan": {"urgent": [], "regular_monitoring": [], "self_monitoring": []},
                "evidence_based_recommendations": []
            }

        prompt = f"""You are a medical assistant. Analyze the following symptoms and return a JSON response.

    Symptoms: {symptoms}

    Return ONLY valid JSON with this exact structure:
    {{
        "psychological_support": "supportive text for the patient",
        "diagnosis_summary": "diagnosis explained in plain language",
        "doctor_questions": ["question1", "question2"],
        "examination_plan": {{
            "urgent": ["exam1"],
            "regular_monitoring": ["exam2"],
            "self_monitoring": ["exam3"]
        }},
        "evidence_based_recommendations": [
            {{"title": "rec1", "recommendation": "text", "benefit": "benefit", "source": "WHO"}}
        ]
    }}"""

        response = self._client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
