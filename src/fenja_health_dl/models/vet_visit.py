from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fenja_health_dl.db import Base

if TYPE_CHECKING:
    from fenja_health_dl.models.treatment import TreatmentProtocol


class VetVisit(Base):
    """Veterinary appointments and their outcomes for Fenja."""

    __tablename__ = "vet_visits"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    reason: Mapped[str] = mapped_column(Text, nullable=False)
    vet_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    clinic: Mapped[str | None] = mapped_column(Text, nullable=True)
    diagnosis: Mapped[str | None] = mapped_column(Text, nullable=True)
    findings: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_appointment: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Protokolle die bei diesem Besuch verschrieben wurden
    protocols: Mapped[list[TreatmentProtocol]] = relationship(
        "TreatmentProtocol", back_populates="vet_visit"
    )
