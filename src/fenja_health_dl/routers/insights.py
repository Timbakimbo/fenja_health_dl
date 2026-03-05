from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from fenja_health_dl.auth import verify_api_key
from fenja_health_dl.db import get_db
from fenja_health_dl.models import DailyLog, HealthMarker, TreatmentEntry, TreatmentProtocol, VitalReading
from fenja_health_dl.schemas.insights import (
    B12TrendPoint,
    ComplianceReport,
    MonthlySummary,
    StoolTrendPoint,
    WeeklySummary,
    WeightTrendPoint,
)

router = APIRouter(
    prefix="/api/insights",
    tags=["insights"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/weight-trend", response_model=list[WeightTrendPoint])
def weight_trend(db: Session = Depends(get_db)):
    points: list[WeightTrendPoint] = []

    # From HealthMarker
    markers = db.query(HealthMarker).filter(HealthMarker.weight_kg.isnot(None)).all()
    for m in markers:
        points.append(WeightTrendPoint(timestamp=m.timestamp, weight_kg=m.weight_kg, source="health_marker"))

    # From VitalReading
    readings = db.query(VitalReading).filter(VitalReading.marker_type == "weight").all()
    for r in readings:
        points.append(WeightTrendPoint(timestamp=r.timestamp, weight_kg=r.value, source="vital_reading"))

    points.sort(key=lambda p: p.timestamp)
    return points


@router.get("/b12-trend", response_model=list[B12TrendPoint])
def b12_trend(db: Session = Depends(get_db)):
    markers = (
        db.query(HealthMarker)
        .filter(HealthMarker.cobalamin_b12.isnot(None))
        .order_by(HealthMarker.timestamp)
        .all()
    )
    return [B12TrendPoint(timestamp=m.timestamp, cobalamin_b12=m.cobalamin_b12) for m in markers]


@router.get("/stool-trend", response_model=list[StoolTrendPoint])
def stool_trend(db: Session = Depends(get_db)):
    logs = (
        db.query(DailyLog)
        .filter(DailyLog.stool_consistency.isnot(None))
        .order_by(DailyLog.date)
        .all()
    )
    return [StoolTrendPoint(date=l.date, stool_consistency=l.stool_consistency, stool_color=l.stool_color) for l in logs]


@router.get("/weekly-summary", response_model=WeeklySummary)
def weekly_summary(
    date_param: date = Query(alias="date", default=None),
    db: Session = Depends(get_db),
):
    target = date_param or date.today()
    # ISO week: Monday to Sunday
    week_start = target - timedelta(days=target.weekday())
    week_end = week_start + timedelta(days=6)

    logs = db.query(DailyLog).filter(DailyLog.date >= week_start, DailyLog.date <= week_end).all()

    days_logged = len(logs)
    energy_vals = [l.energy_level for l in logs if l.energy_level is not None]
    stool_vals = [l.stool_consistency for l in logs if l.stool_consistency is not None]
    appetite_vals = [l.appetite_ratio for l in logs if l.appetite_ratio is not None]
    pain_vals = [l.pain_score for l in logs if l.pain_score is not None]
    vomiting_episodes = sum(1 for l in logs if l.vomiting)

    return WeeklySummary(
        week_start=week_start,
        week_end=week_end,
        days_logged=days_logged,
        avg_energy_level=round(sum(energy_vals) / len(energy_vals), 2) if energy_vals else None,
        avg_stool_consistency=round(sum(stool_vals) / len(stool_vals), 2) if stool_vals else None,
        avg_appetite_ratio=round(sum(appetite_vals) / len(appetite_vals), 2) if appetite_vals else None,
        total_vomiting_episodes=vomiting_episodes,
        avg_pain_score=round(sum(pain_vals) / len(pain_vals), 2) if pain_vals else None,
        max_pain_score=max(pain_vals) if pain_vals else None,
    )


@router.get("/monthly-summary", response_model=MonthlySummary)
def monthly_summary(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
):
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(year, month + 1, 1) - timedelta(days=1)

    logs = db.query(DailyLog).filter(DailyLog.date >= month_start, DailyLog.date <= month_end).all()

    days_logged = len(logs)
    energy_vals = [l.energy_level for l in logs if l.energy_level is not None]
    stool_vals = [l.stool_consistency for l in logs if l.stool_consistency is not None]
    appetite_vals = [l.appetite_ratio for l in logs if l.appetite_ratio is not None]
    pain_vals = [l.pain_score for l in logs if l.pain_score is not None]
    vomiting_episodes = sum(1 for l in logs if l.vomiting)

    # Weight change: first vs last HealthMarker in the month
    weight_markers = (
        db.query(HealthMarker)
        .filter(
            HealthMarker.weight_kg.isnot(None),
            func.date(HealthMarker.timestamp) >= month_start,
            func.date(HealthMarker.timestamp) <= month_end,
        )
        .order_by(HealthMarker.timestamp)
        .all()
    )
    weight_start = weight_markers[0].weight_kg if weight_markers else None
    weight_end = weight_markers[-1].weight_kg if weight_markers else None
    weight_change = round(weight_end - weight_start, 2) if weight_start is not None and weight_end is not None else None

    return MonthlySummary(
        week_start=month_start,
        week_end=month_end,
        days_logged=days_logged,
        avg_energy_level=round(sum(energy_vals) / len(energy_vals), 2) if energy_vals else None,
        avg_stool_consistency=round(sum(stool_vals) / len(stool_vals), 2) if stool_vals else None,
        avg_appetite_ratio=round(sum(appetite_vals) / len(appetite_vals), 2) if appetite_vals else None,
        total_vomiting_episodes=vomiting_episodes,
        avg_pain_score=round(sum(pain_vals) / len(pain_vals), 2) if pain_vals else None,
        max_pain_score=max(pain_vals) if pain_vals else None,
        weight_start_kg=weight_start,
        weight_end_kg=weight_end,
        weight_change_kg=weight_change,
    )


@router.get("/treatment-compliance", response_model=ComplianceReport)
def treatment_compliance(
    protocol_id: int = Query(...),
    db: Session = Depends(get_db),
):
    protocol = db.get(TreatmentProtocol, protocol_id)
    if not protocol:
        from fenja_health_dl.errors import resource_not_found
        raise resource_not_found("TreatmentProtocol", protocol_id)

    entries = db.query(TreatmentEntry).filter(TreatmentEntry.protocol_id == protocol_id).all()

    total = len(entries)
    administered = sum(1 for e in entries if e.administered_at is not None)
    skipped = sum(1 for e in entries if e.was_skipped)
    pending = total - administered - skipped

    compliance_rate = round(administered / (administered + skipped), 2) if (administered + skipped) > 0 else 0.0

    return ComplianceReport(
        protocol_id=protocol.id,
        protocol_name=protocol.name,
        total_entries=total,
        administered=administered,
        skipped=skipped,
        pending=pending,
        compliance_rate=compliance_rate,
    )
