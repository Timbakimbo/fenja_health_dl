import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from fenja_health_dl.errors import handle_integrity_error
from fenja_health_dl.model import predict_risk, reload_model, get_model_snapshot
from fenja_health_dl.routers import daily_logs, health_markers, insights, treatments, vet_visits, vital_readings


def _frontend_origins() -> list[str]:
    default_origins = {
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    }
    extra_origins = {
        origin.strip()
        for origin in os.environ.get("FRONTEND_ORIGINS", "").split(",")
        if origin.strip()
    }
    return sorted(default_origins | extra_origins)

app = FastAPI(title="Fenja Health DL", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_frontend_origins(),
    allow_origin_regex=(
        r"^https://.*\.(trycloudflare\.com|ngrok-free\.app|ngrok\.app)$|"
        r"^https?://(localhost|127\.0\.0\.1)"
        r"(?::\d{1,5})?$|"
        r"^https?://("
        r"10(?:\.\d{1,3}){3}|"
        r"192\.168(?:\.\d{1,3}){2}|"
        r"172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}"
        r")(?::\d{1,5})?$"
    ),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(IntegrityError, handle_integrity_error)

# CRUD routers
app.include_router(health_markers.router)
app.include_router(daily_logs.router)
app.include_router(treatments.templates_router)
app.include_router(treatments.protocols_router)
app.include_router(vet_visits.router)
app.include_router(vital_readings.router)
app.include_router(insights.router)


# Legacy endpoints (unprotected)
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
