from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


# --- TreatmentTemplate ---

class TreatmentTemplateCreate(BaseModel):
    name: str
    category: str
    default_schedule: dict[str, Any]
    notes: str | None = None


class TreatmentTemplateUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    default_schedule: dict[str, Any] | None = None
    notes: str | None = None


class TreatmentTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    default_schedule: dict[str, Any]
    notes: str | None = None
    created_at: datetime


# --- TreatmentEntry ---

class TreatmentEntryCreate(BaseModel):
    scheduled_date: date
    administered_at: datetime | None = None
    dose: float | None = None
    unit: str | None = None
    administered_by: str | None = None
    notes: str | None = None


class TreatmentEntryUpdate(BaseModel):
    scheduled_date: date | None = None
    administered_at: datetime | None = None
    dose: float | None = None
    unit: str | None = None
    administered_by: str | None = None
    notes: str | None = None


class TreatmentEntryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    protocol_id: int
    scheduled_date: date
    administered_at: datetime | None = None
    dose: float | None = None
    unit: str | None = None
    administered_by: str | None = None
    notes: str | None = None
    created_at: datetime
    was_skipped: bool


# --- TreatmentProtocol ---

class TreatmentProtocolCreate(BaseModel):
    template_id: int | None = None
    vet_visit_id: int | None = None
    category: str
    name: str
    schedule: dict[str, Any]
    start_date: date
    end_date: date | None = None
    prescribed_by: str | None = None
    active: bool = True
    notes: str | None = None


class TreatmentProtocolUpdate(BaseModel):
    template_id: int | None = None
    vet_visit_id: int | None = None
    category: str | None = None
    name: str | None = None
    schedule: dict[str, Any] | None = None
    start_date: date | None = None
    end_date: date | None = None
    prescribed_by: str | None = None
    active: bool | None = None
    notes: str | None = None


class TreatmentProtocolRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    template_id: int | None = None
    vet_visit_id: int | None = None
    category: str
    name: str
    schedule: dict[str, Any]
    start_date: date
    end_date: date | None = None
    prescribed_by: str | None = None
    active: bool
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    current_phase: dict[str, Any] | None = None
    entries: list[TreatmentEntryRead] = []
