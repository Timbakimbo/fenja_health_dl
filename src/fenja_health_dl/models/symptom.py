"""
Symptom daily tracking model for Fenja.

Architecture Decision (März 2026):
Wir nutzen ein Hybrid-Schema: DailyLog für tägliche Kernwerte +
SymptomObservation für flexible Zusatzbeobachtungen.

Evaluierte Alternativen:
- Column Family Stores (Cassandra/ScyllaDB): Optimal für sparse
  time-series data, abgelehnt wegen Ops-Overhead – Overengineering
  für einen einzelnen Patienten.
- TimescaleDB: Guter Mittelweg, abgelehnt weil Standard-PostgreSQL
  für aktuellen Datensatz ausreicht.

Revisit wenn: Mehrere Patienten oder Wearable-Daten im Minutentakt
→ dann TimescaleDB oder Cassandra evaluieren.
"""

from datetime import date, datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fenja_health_dl.db import Base


class DailyLog(Base):
    """
    Ein Eintrag pro Tag – die Kernwerte die täglich getrackt werden.
    Bewusst schlank gehalten: nur was wirklich jeden Tag relevant ist.
    Seltene/unregelmäßige Symptome kommen in SymptomObservation.
    """

    __tablename__ = "daily_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # date weil ein Eintrag pro Tag
    # unique=True verhindert versehentliche Doppeleinträge für denselben Tag
    date: Mapped[date] = mapped_column(Date, nullable=False, unique=True)

    # === ERNÄHRUNG ===
    # Objektiv messbar → kein subjektiver Bias wie bei einer 1-5 Skala
    # appetite_ratio wird in API berechnet: food_eaten_g / food_offered_g
    food_offered_g: Mapped[float | None] = mapped_column(Float, nullable=True)
    food_eaten_g: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Wasseraufnahme : subjektiv – schwer in Gramm zu messen im Alltag
    water_intake: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="normal | erhöht | reduziert"
    )

    # === VERDAUUNG (EPI-spezifisch) ===
    # Angelehnt an Bristol Stool Scale – international standardisiert
    # 1 = sehr fest, 5 = wässrig/durchfall
    stool_consistency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    stool_color: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="normal | blass | fettig | dunkel"
    )
    # Boolean statt Skala – Flatulenz ist entweder da oder nicht
    flatulence: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    vomiting: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # Anzahl nur relevant wenn vomiting=True
    vomiting_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # === ENERGIE & VERHALTEN ===
    # 1-5 Skala: 1 = apathisch, 5 = vollaktiv
    energy_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    willingness_to_walk: Mapped[int | None] = mapped_column(Integer, nullable=True)
    play_interest: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # === ÄUSSERES ERSCHEINUNGSBILD ===
    # Fell und Muskel wichtig bei EPI – Malabsorption sieht man am Erscheinungsbild
    coat_condition: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # muscle_wasting: 1 = stark abgebaut, 5 = gute Muskulatur
    muscle_wasting: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # === ORTHOPÄDIE ===
    # Veterinäre Lahmheitsskala: 0 = keine Lahmheit, 4 = keine Belastung
    lameness_score: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="0=keine Lahmheit, 4=keine Belastung"
    )
    # Welches Bein? VL=vorne links, VR=vorne rechts, HL=hinten links, HR=hinten rechts
    affected_limb: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="VL | VR | HL | HR"
    )
    # Typisches HD-Symptom: Steifheit nach Ruhe, bessert sich nach Aufwärmen
    stiffness_after_rest: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # === SCHMERZ (angelehnt an Glasgow CMPS-SF) ===
    # Glasgow Composite Measure Pain Scale Short Form: validierte veterinäre Schmerzskala
    # Max 24 Punkte. Intervention empfohlen ab Score >= 6
    pain_score: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="Glasgow CMPS-SF: 0-24, Intervention ab 6"
    )
    #freitext für Schmerzlokalisation, z.B. "Rücken", "Hüfte", "Knie"
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamp für Audit-Trail – wann wurde der Eintrag erstellt/geändert
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationship zu SymptomObservation – ein DailyLog hat viele Observations
    observations: Mapped[list["SymptomObservation"]] = relationship(
        "SymptomObservation", back_populates="daily_log", cascade="all, delete-orphan"
    )

    __table_args__ = (
        # DB-seitige Constraints – verhindert ungültige Werte auch ohne API
        CheckConstraint("stool_consistency BETWEEN 1 AND 5", name="ck_stool_1_5"),
        CheckConstraint("energy_level BETWEEN 1 AND 5", name="ck_energy_1_5"),
        CheckConstraint("willingness_to_walk BETWEEN 1 AND 5", name="ck_walk_1_5"),
        CheckConstraint("play_interest BETWEEN 1 AND 5", name="ck_play_1_5"),
        CheckConstraint("coat_condition BETWEEN 1 AND 5", name="ck_coat_1_5"),
        CheckConstraint("muscle_wasting BETWEEN 1 AND 5", name="ck_muscle_1_5"),
        CheckConstraint("lameness_score BETWEEN 0 AND 4", name="ck_lameness_0_4"),
        CheckConstraint("pain_score BETWEEN 0 AND 24", name="ck_pain_0_24"),
        CheckConstraint("vomiting_count >= 0", name="ck_vomiting_count_pos"),
    )
    #methode zu attribut 
    @property
    def appetite_ratio(self) -> float | None:
        """
        Objektiver Appetit-Index: 1.0 = alles gefressen, 0.0 = nichts gefressen.
        Besser als subjektive 1-5 Skala weil direkt aus Messwerten berechnet.
        """
        if self.food_offered_g and self.food_eaten_g:
            return round(self.food_eaten_g / self.food_offered_g, 2)
        return None


class SymptomObservation(Base):
    """
    Flexible Zusatzbeobachtungen die nicht täglich vorkommen.
    Key-Value Struktur – kein Schema-Change nötig für neue Symptomtypen.
    Beispiele: "hautausschlag", "niesen", "zittern", "augenausfluss"
    """

    __tablename__ = "symptom_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign Key zu DailyLog – jede Observation gehört zu einem Tag
    daily_log_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("daily_logs.id"), nullable=False
    )

    # Freitext-Typ – keine Enum damit neue Symptome ohne Migration möglich sind
    symptom_type: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="z.B. hautausschlag, niesen, zittern"
    )

    # Drei Wert-Typen – je nach Symptom wird nur einer befüllt, Rest bleibt NULL
    value_numeric: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_text: Mapped[str | None] = mapped_column(String(200), nullable=True)
    value_bool: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Rückbeziehung zu DailyLog
    # Relationship definiert Verbindung von SymptomObservation zurück zum DailyLog, back_populates sorgt dafür, dass wir von DailyLog aus auch auf die Observations zugreifen können, Achtung Cascade in Dailylog. 
    daily_log: Mapped["DailyLog"] = relationship(
        "DailyLog", back_populates="observations"
    )
