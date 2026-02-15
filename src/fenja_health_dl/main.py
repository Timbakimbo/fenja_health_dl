from fastapi import FastAPI
from pydantic import BaseModel
from fenja_health_dl.preprocessing import compute_risk
from fenja_health_dl.model import MODEL

app = FastAPI()

class model_input(BaseModel):
    weight: float
    age: int
    activity: int

@app.get("/")
def root():
    return {"message": "Fenja AI läuft 🐕"}

@app.post("/predict")
def predict(data: model_input):
    risk = MODEL.predict_risk(data.age, data.activity, data.weight)
    return {"risk_score": round(risk, 2)}