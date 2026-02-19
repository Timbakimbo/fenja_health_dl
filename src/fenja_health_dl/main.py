from fastapi import FastAPI
from pydantic import BaseModel

from fenja_health_dl.model import predict_risk, reload_model, get_model_snapshot

app = FastAPI()


class ModelInput(BaseModel):
    weight: float
    age: int
    activity: int


@app.get("/")
def root():
    return {"message": "Fenja AI läuft 🐕"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/model/reload")
def model_reload():
    model = reload_model()
    return {"reloaded": True, "model": model}


@app.post("/predict")
def predict(data: ModelInput):
    risk = predict_risk(data.age, data.activity, data.weight)
    return {"risk_score": round(risk, 2)}
