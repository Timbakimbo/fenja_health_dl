# ADR: Diese Tabelle ist für kontinuierliche / device-basierte Daten gedacht
# (Halsband, Waage, CV-Modell). Getrennt von HealthMarker weil andere Frequenz
# und anderer Ursprung. Erweiterbar für Meta Glasses / Wearables ohne Schema-Änderung
# durch den freien marker_type + source String.
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from fenja_health_dl.db import Base


class VitalReading(Base):
    """Continuous / device-sourced measurements for Fenja."""

    __tablename__ = "vital_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # e.g. "heart_rate", "temperature", "weight", "respiratory_rate"
    marker_type: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    # e.g. "bpm", "°C", "kg", "breaths/min"
    unit: Mapped[str] = mapped_column(Text, nullable=False)
    # e.g. "halsband", "waage", "manual", "cv_model", "meta_glasses"
    source: Mapped[str] = mapped_column(Text, nullable=False)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
