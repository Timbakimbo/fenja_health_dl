from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# --- SymptomObservation Schemas ---

class SymptomObservationCreate(BaseModel):
    daily_log_id: int
    symptom_type: str
    value_numeric: float | None = None
    value_text: str | None = None
    value_bool: bool | None = None
    notes: str | None = None


class SymptomObservationNested(BaseModel):
    """Create schema without daily_log_id (comes from URL path)."""
    symptom_type: str
    value_numeric: float | None = None
    value_text: str | None = None
    value_bool: bool | None = None
    notes: str | None = None


class SymptomObservationUpdate(BaseModel):
    symptom_type: str | None = None
    value_numeric: float | None = None
    value_text: str | None = None
    value_bool: bool | None = None
    notes: str | None = None


class SymptomObservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    daily_log_id: int
    symptom_type: str
    value_numeric: float | None = None
    value_text: str | None = None
    value_bool: bool | None = None
    notes: str | None = None
    timestamp: datetime


# --- DailyLog Schemas ---

class DailyLogCreate(BaseModel):
    date: date
    food_offered_g: float | None = None
    food_eaten_g: float | None = None
    water_intake: str | None = None
    stool_consistency: int | None = Field(None, ge=1, le=5)
    stool_color: str | None = None
    flatulence: bool | None = None
    vomiting: bool | None = None
    vomiting_count: int | None = Field(None, ge=0)
    energy_level: int | None = Field(None, ge=1, le=5)
    willingness_to_walk: int | None = Field(None, ge=1, le=5)
    play_interest: int | None = Field(None, ge=1, le=5)
    coat_condition: int | None = Field(None, ge=1, le=5)
    muscle_wasting: int | None = Field(None, ge=1, le=5)
    lameness_score: int | None = Field(None, ge=0, le=4)
    affected_limb: str | None = None
    stiffness_after_rest: bool | None = None
    pain_score: int | None = Field(None, ge=0, le=24)
    notes: str | None = None


class DailyLogUpdate(BaseModel):
    food_offered_g: float | None = None
    food_eaten_g: float | None = None
    water_intake: str | None = None
    stool_consistency: int | None = Field(None, ge=1, le=5)
    stool_color: str | None = None
    flatulence: bool | None = None
    vomiting: bool | None = None
    vomiting_count: int | None = Field(None, ge=0)
    energy_level: int | None = Field(None, ge=1, le=5)
    willingness_to_walk: int | None = Field(None, ge=1, le=5)
    play_interest: int | None = Field(None, ge=1, le=5)
    coat_condition: int | None = Field(None, ge=1, le=5)
    muscle_wasting: int | None = Field(None, ge=1, le=5)
    lameness_score: int | None = Field(None, ge=0, le=4)
    affected_limb: str | None = None
    stiffness_after_rest: bool | None = None
    pain_score: int | None = Field(None, ge=0, le=24)
    notes: str | None = None


class DailyLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    created_at: datetime
    food_offered_g: float | None = None
    food_eaten_g: float | None = None
    water_intake: str | None = None
    stool_consistency: int | None = None
    stool_color: str | None = None
    flatulence: bool | None = None
    vomiting: bool | None = None
    vomiting_count: int | None = None
    energy_level: int | None = None
    willingness_to_walk: int | None = None
    play_interest: int | None = None
    coat_condition: int | None = None
    muscle_wasting: int | None = None
    lameness_score: int | None = None
    affected_limb: str | None = None
    stiffness_after_rest: bool | None = None
    pain_score: int | None = None
    notes: str | None = None
    appetite_ratio: float | None = None
    observations: list[SymptomObservationRead] = []
