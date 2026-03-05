from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from fenja_health_dl.auth import verify_api_key
from fenja_health_dl.db import get_db
from fenja_health_dl.errors import resource_not_found
from fenja_health_dl.models import VitalReading
from fenja_health_dl.schemas.pagination import DEFAULT_PAGE_SIZE, PaginatedResponse, clamp_page_size
from fenja_health_dl.schemas.vital_reading import VitalReadingCreate, VitalReadingRead, VitalReadingUpdate

router = APIRouter(
    prefix="/api/vital-readings",
    tags=["vital-readings"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/", response_model=PaginatedResponse[VitalReadingRead])
def list_vital_readings(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    marker_type: str | None = None,
    source: str | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_db),
):
    page_size = clamp_page_size(page_size)
    q = db.query(VitalReading)
    if marker_type:
        q = q.filter(VitalReading.marker_type == marker_type)
    if source:
        q = q.filter(VitalReading.source == source)
    if from_date:
        q = q.filter(VitalReading.timestamp >= from_date)
    if to_date:
        q = q.filter(VitalReading.timestamp <= to_date)
    total = q.count()
    items = q.order_by(VitalReading.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.post("/", response_model=VitalReadingRead, status_code=status.HTTP_201_CREATED)
def create_vital_reading(data: VitalReadingCreate, db: Session = Depends(get_db)):
    obj = VitalReading(**data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{reading_id}", response_model=VitalReadingRead)
def get_vital_reading(reading_id: int, db: Session = Depends(get_db)):
    obj = db.get(VitalReading, reading_id)
    if not obj:
        raise resource_not_found("VitalReading", reading_id)
    return obj


@router.patch("/{reading_id}", response_model=VitalReadingRead)
def update_vital_reading(reading_id: int, data: VitalReadingUpdate, db: Session = Depends(get_db)):
    obj = db.get(VitalReading, reading_id)
    if not obj:
        raise resource_not_found("VitalReading", reading_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vital_reading(reading_id: int, db: Session = Depends(get_db)):
    obj = db.get(VitalReading, reading_id)
    if not obj:
        raise resource_not_found("VitalReading", reading_id)
    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
