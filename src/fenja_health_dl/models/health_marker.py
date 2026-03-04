from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from fenja_health_dl.db import Base
#Laborwerte (feste Struktur und klinische Referenzwerte)

#erbt von Base, damit SQLAlchemy weiß, dass es eine Tabelle in der DB ist
class HealthMarker(Base):
    """Lab results and weight measurements for Fenja."""

    __tablename__ = "health_markers"
    #id ist TypeHint, mapped_coloumn ist die SQLAlchemy Def der DB-SPalte, primary_key=True -> PostgreSQL generiert automatisch eine eindeutige ID für jeden Eintrag
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    #wieder TypeHint, mapped_column definiert die Spalte, default ist aktueller Zeitstempel in UTC, damit wir wissen, wann die Messung gemacht wurde.
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Physical
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)

    # EPI / pancreas markers
    ctli: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Canine TLI in µg/L; EPI threshold < 2.5")
    lipase: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Lipase in U/L")
    amylase: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Amylase in U/L")

    # B12 / folate (key for EPI secondary deficiencies)
    cobalamin_b12: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Cobalamin B12 in pg/mL")
    folate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Folate in µg/L")

    # Metabolic
    glucose: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Glucose in mg/dL")

    # Fat-soluble vitamins (often depleted in EPI)
    vitamin_e: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Vitamin E in mg/L")
    vitamin_k: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Vitamin K in µg/L")
