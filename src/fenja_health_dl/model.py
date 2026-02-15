import json
from dataclasses import dataclass
from pathlib import Path

MODEL_PATH = Path("models/risk_model.json")


@dataclass
class RiskModel:
    bias: float = 0.0

    def predict_risk(self, age: int, activity: int, weight: float) -> float:
        return (age + (10 - activity)) / 20 + self.bias

    def save(self) -> None:
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(MODEL_PATH, "w") as f:
            json.dump({"bias": self.bias}, f)

    @classmethod
    def load(cls) -> "RiskModel":
        if MODEL_PATH.exists():
            with open(MODEL_PATH) as f:
                data = json.load(f)
            return cls(**data)
        return cls()


MODEL = RiskModel.load()


