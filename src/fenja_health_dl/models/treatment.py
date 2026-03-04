"""
Treatment-Modelle für Fenjas Therapiepläne.

Architecture Decision (März 2026):
Dreistufiges Schema: Template → Protocol → Entry

TreatmentTemplate: Wiederverwendbare Vorlage (z.B. "Standard B12 Injektion Schema").
  Definiert den default_schedule – eine JSONB-Struktur die phasenbasierte
  Dosierungen oder Übungspläne beschreibt.

TreatmentProtocol: Konkrete Verschreibung für Fenja, abgeleitet aus einem Template
  (oder frei erstellt). schedule wird aus Template kopiert und kann angepasst werden.
  Verknüpft optional mit dem VetVisit bei dem es verschrieben wurde.
  current_phase berechnet dynamisch die aktuelle Phase aus schedule + start_date.

TreatmentEntry: Jede tatsächliche Gabe / Durchführung (oder bewusstes Überspringen).
  was_skipped als @property: scheduled_date vergangen und administered_at ist None.

Evaluierte Alternativen:
- Flache Tabelle mit Enum-Typ: Zu unflexibel für die B12-Injektions-Phasen
  (Wochen 1-6: täglich, dann 14-tägig) und Physio-Übungspläne gleichzeitig.
- Separate Tabellen pro Behandlungstyp: Overengineering für einen Patienten,
  schwer zu erweitern für neue Therapieformen (z.B. Physiotherapie, Diät).
- JSONB für alles (EAV-Ansatz): Zu wenig Struktur, schlechte Querybarkeit
  für Auswertungen (wann war letzte Gabe, Compliance-Rate etc.).

schedule JSONB-Beispiele:
  B12-Injektionsprotokoll:
    {"type": "injection_protocol", "phases": [
      {"weeks": 6, "interval_days": 7, "dose": 1.0, "unit": "ml"},
      {"weeks": null, "interval_days": 14, "dose": 1.0, "unit": "ml"}
    ]}
  Physiotherapie-Heimplan:
    {"type": "daily_exercise", "frequency": "2x täglich", "exercises": [
      {"name": "Gewichtsverlagerung HL", "sets": 3, "reps": 10},
      {"name": "Cavaletti", "duration_minutes": 5},
      {"name": "Treppe rauf/runter", "reps": 5, "supervised": true}
    ]}
"""

from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fenja_health_dl.db import Base


class TreatmentTemplate(Base):
    """
    Wiederverwendbare Therapievorlage.
    Enthält den default_schedule den Tierärzte für Standardprotokolle definieren.
    """

    __tablename__ = "treatment_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Eindeutiger Name damit Templates referenzierbar sind
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    # Freitext-Kategorie – kein Enum damit neue Typen ohne Migration möglich
    # z.B. "b12", "enzyme", "antibiotic", "exercise", "diet"
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    # Vorlage für den Schedule – wird bei Protokollerstellung kopiert
    default_schedule: Mapped[dict] = mapped_column(JSONB, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    protocols: Mapped[list["TreatmentProtocol"]] = relationship(
        "TreatmentProtocol", back_populates="template"
    )


class TreatmentProtocol(Base):
    """
    Konkrete aktive oder vergangene Therapie für Fenja.
    Kann aus einem Template erzeugt werden (schedule wird kopiert, dann anpassbar)
    oder ohne Template erstellt werden (z.B. einmalige Antibiotika-Kur).
    """

    __tablename__ = "treatment_protocols"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Optionale Verknüpfung mit Template – nullable weil Freiprotokolle möglich
    template_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("treatment_templates.id"), nullable=True
    )
    # Optionale Verknüpfung mit dem Tierarztbesuch bei dem das Protokoll verschrieben wurde
    vet_visit_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("vet_visits.id"), nullable=True
    )

    category: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Kopie des Template-Schedules, danach individuell anpassbar
    schedule: Mapped[dict] = mapped_column(JSONB, nullable=False)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    prescribed_by: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # False = archiviert/abgeschlossen
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    template: Mapped["TreatmentTemplate | None"] = relationship(
        "TreatmentTemplate", back_populates="protocols"
    )
    vet_visit: Mapped["VetVisit | None"] = relationship(  # type: ignore[name-defined]
        "VetVisit", back_populates="protocols"
    )
    entries: Mapped[list["TreatmentEntry"]] = relationship(
        "TreatmentEntry", back_populates="protocol", cascade="all, delete-orphan"
    )

    @property
    def current_phase(self) -> dict | None:
        """
        Berechnet die aktuelle Phase aus schedule + start_date.
        Für Injektionsprotokolle mit Phasen: findet die Phase basierend auf vergangenen Wochen.
        Für andere Schedule-Typen (z.B. Übungspläne): gibt den gesamten Schedule zurück.
        """
        if not self.schedule or "phases" not in self.schedule:
            return self.schedule

        elapsed_weeks = (date.today() - self.start_date).days / 7
        accumulated = 0.0
        for phase in self.schedule["phases"]:
            if phase.get("weeks") is None:
                # Terminale / Erhaltungsphase – gilt für immer
                return phase
            accumulated += phase["weeks"]
            if elapsed_weeks < accumulated:
                return phase

        # Fallback: letzte definierte Phase
        return self.schedule["phases"][-1]


class TreatmentEntry(Base):
    """
    Einzelne Gabe oder bewusstes Überspringen einer Behandlung.
    scheduled_date ist das geplante Datum; administered_at ist der tatsächliche Zeitpunkt.
    Wenn scheduled_date vergangen und administered_at=None → was_skipped=True.
    """

    __tablename__ = "treatment_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    protocol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("treatment_protocols.id"), nullable=False
    )

    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    # None = noch nicht verabreicht oder übersprungen
    administered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    dose: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # z.B. "owner", "vet", "tierpfleger"
    administered_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    protocol: Mapped["TreatmentProtocol"] = relationship(
        "TreatmentProtocol", back_populates="entries"
    )

    @property
    def was_skipped(self) -> bool:
        """True wenn das geplante Datum vergangen ist aber keine Gabe dokumentiert wurde."""
        return self.administered_at is None and self.scheduled_date < date.today()
