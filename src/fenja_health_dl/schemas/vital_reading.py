from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VitalReadingCreate(BaseModel):
    marker_type: str
    value: float
    unit: str
    source: str
    timestamp: datetime | None = None
    notes: str | None = None


class VitalReadingUpdate(BaseModel):
    marker_type: str | None = None
    value: float | None = None
    unit: str | None = None
    source: str | None = None
    notes: str | None = None


class VitalReadingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    marker_type: str
    value: float
    unit: str
    source: str
    notes: str | None = None
