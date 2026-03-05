from datetime import datetime

from pydantic import BaseModel, ConfigDict

from fenja_health_dl.schemas.treatment import TreatmentProtocolRead


class VetVisitCreate(BaseModel):
    reason: str
    vet_name: str | None = None
    clinic: str | None = None
    diagnosis: str | None = None
    findings: str | None = None
    next_appointment: datetime | None = None
    notes: str | None = None
    timestamp: datetime | None = None


class VetVisitUpdate(BaseModel):
    reason: str | None = None
    vet_name: str | None = None
    clinic: str | None = None
    diagnosis: str | None = None
    findings: str | None = None
    next_appointment: datetime | None = None
    notes: str | None = None


class VetVisitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    reason: str
    vet_name: str | None = None
    clinic: str | None = None
    diagnosis: str | None = None
    findings: str | None = None
    next_appointment: datetime | None = None
    notes: str | None = None
    protocols: list[TreatmentProtocolRead] = []
