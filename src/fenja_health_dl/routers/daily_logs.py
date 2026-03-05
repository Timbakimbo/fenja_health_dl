from datetime import date

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from fenja_health_dl.auth import verify_api_key
from fenja_health_dl.db import get_db
from fenja_health_dl.errors import resource_not_found
from fenja_health_dl.models import DailyLog, SymptomObservation
from fenja_health_dl.schemas.daily_log import (
    DailyLogCreate,
    DailyLogRead,
    DailyLogUpdate,
    SymptomObservationNested,
    SymptomObservationRead,
    SymptomObservationUpdate,
)
from fenja_health_dl.schemas.pagination import DEFAULT_PAGE_SIZE, PaginatedResponse, clamp_page_size

router = APIRouter(
    prefix="/api/daily-logs",
    tags=["daily-logs"],
    dependencies=[Depends(verify_api_key)],
)


# --- DailyLog CRUD ---

@router.get("/", response_model=PaginatedResponse[DailyLogRead])
def list_daily_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
):
    page_size = clamp_page_size(page_size)
    q = db.query(DailyLog)
    if from_date:
        q = q.filter(DailyLog.date >= from_date)
    if to_date:
        q = q.filter(DailyLog.date <= to_date)
    total = q.count()
    items = q.order_by(DailyLog.date.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.post("/", response_model=DailyLogRead, status_code=status.HTTP_201_CREATED)
def create_daily_log(data: DailyLogCreate, db: Session = Depends(get_db)):
    obj = DailyLog(**data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{log_id}", response_model=DailyLogRead)
def get_daily_log(log_id: int, db: Session = Depends(get_db)):
    obj = db.get(DailyLog, log_id)
    if not obj:
        raise resource_not_found("DailyLog", log_id)
    return obj


@router.patch("/{log_id}", response_model=DailyLogRead)
def update_daily_log(log_id: int, data: DailyLogUpdate, db: Session = Depends(get_db)):
    obj = db.get(DailyLog, log_id)
    if not obj:
        raise resource_not_found("DailyLog", log_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_log(log_id: int, db: Session = Depends(get_db)):
    obj = db.get(DailyLog, log_id)
    if not obj:
        raise resource_not_found("DailyLog", log_id)
    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Nested Observations ---

def _get_log_or_404(log_id: int, db: Session) -> DailyLog:
    obj = db.get(DailyLog, log_id)
    if not obj:
        raise resource_not_found("DailyLog", log_id)
    return obj


def _get_observation_or_404(log_id: int, obs_id: int, db: Session) -> SymptomObservation:
    obs = db.query(SymptomObservation).filter(
        SymptomObservation.id == obs_id,
        SymptomObservation.daily_log_id == log_id,
    ).first()
    if not obs:
        raise resource_not_found("SymptomObservation", obs_id)
    return obs


@router.get("/{log_id}/observations", response_model=PaginatedResponse[SymptomObservationRead])
def list_observations(
    log_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    db: Session = Depends(get_db),
):
    _get_log_or_404(log_id, db)
    page_size = clamp_page_size(page_size)
    q = db.query(SymptomObservation).filter(SymptomObservation.daily_log_id == log_id)
    total = q.count()
    items = q.order_by(SymptomObservation.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.post("/{log_id}/observations", response_model=SymptomObservationRead, status_code=status.HTTP_201_CREATED)
def create_observation(log_id: int, data: SymptomObservationNested, db: Session = Depends(get_db)):
    _get_log_or_404(log_id, db)
    obj = SymptomObservation(daily_log_id=log_id, **data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{log_id}/observations/{obs_id}", response_model=SymptomObservationRead)
def get_observation(log_id: int, obs_id: int, db: Session = Depends(get_db)):
    return _get_observation_or_404(log_id, obs_id, db)


@router.patch("/{log_id}/observations/{obs_id}", response_model=SymptomObservationRead)
def update_observation(log_id: int, obs_id: int, data: SymptomObservationUpdate, db: Session = Depends(get_db)):
    obs = _get_observation_or_404(log_id, obs_id, db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obs, key, value)
    db.commit()
    db.refresh(obs)
    return obs


@router.delete("/{log_id}/observations/{obs_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_observation(log_id: int, obs_id: int, db: Session = Depends(get_db)):
    obs = _get_observation_or_404(log_id, obs_id, db)
    db.delete(obs)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
