from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HealthMarkerCreate(BaseModel):
    weight_kg: float | None = None
    ctli: float | None = None
    lipase: float | None = None
    amylase: float | None = None
    cobalamin_b12: float | None = None
    folate: float | None = None
    glucose: float | None = None
    vitamin_e: float | None = None
    vitamin_k: float | None = None
    timestamp: datetime | None = None


class HealthMarkerUpdate(BaseModel):
    weight_kg: float | None = None
    ctli: float | None = None
    lipase: float | None = None
    amylase: float | None = None
    cobalamin_b12: float | None = None
    folate: float | None = None
    glucose: float | None = None
    vitamin_e: float | None = None
    vitamin_k: float | None = None


class HealthMarkerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    weight_kg: float | None = None
    ctli: float | None = None
    lipase: float | None = None
    amylase: float | None = None
    cobalamin_b12: float | None = None
    folate: float | None = None
    glucose: float | None = None
    vitamin_e: float | None = None
    vitamin_k: float | None = None
