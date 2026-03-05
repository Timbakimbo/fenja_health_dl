from datetime import date, datetime

from pydantic import BaseModel


class WeightTrendPoint(BaseModel):
    timestamp: datetime
    weight_kg: float
    source: str  # "health_marker" or "vital_reading"


class B12TrendPoint(BaseModel):
    timestamp: datetime
    cobalamin_b12: float


class StoolTrendPoint(BaseModel):
    date: date
    stool_consistency: int
    stool_color: str | None = None


class WeeklySummary(BaseModel):
    week_start: date
    week_end: date
    days_logged: int
    avg_energy_level: float | None = None
    avg_stool_consistency: float | None = None
    avg_appetite_ratio: float | None = None
    total_vomiting_episodes: int
    avg_pain_score: float | None = None
    max_pain_score: int | None = None


class MonthlySummary(BaseModel):
    week_start: date
    week_end: date
    days_logged: int
    avg_energy_level: float | None = None
    avg_stool_consistency: float | None = None
    avg_appetite_ratio: float | None = None
    total_vomiting_episodes: int
    avg_pain_score: float | None = None
    max_pain_score: int | None = None
    weight_start_kg: float | None = None
    weight_end_kg: float | None = None
    weight_change_kg: float | None = None


class ComplianceReport(BaseModel):
    protocol_id: int
    protocol_name: str
    total_entries: int
    administered: int
    skipped: int
    pending: int
    compliance_rate: float
