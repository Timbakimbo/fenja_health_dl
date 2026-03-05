from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from fenja_health_dl.auth import verify_api_key
from fenja_health_dl.db import get_db
from fenja_health_dl.errors import resource_not_found
from fenja_health_dl.models import HealthMarker
from fenja_health_dl.schemas.health_marker import HealthMarkerCreate, HealthMarkerRead, HealthMarkerUpdate
from fenja_health_dl.schemas.pagination import DEFAULT_PAGE_SIZE, PaginatedResponse, clamp_page_size

router = APIRouter(
    prefix="/api/health-markers",
    tags=["health-markers"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/", response_model=PaginatedResponse[HealthMarkerRead])
def list_health_markers(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_db),
):
    page_size = clamp_page_size(page_size)
    q = db.query(HealthMarker)
    if from_date:
        q = q.filter(HealthMarker.timestamp >= from_date)
    if to_date:
        q = q.filter(HealthMarker.timestamp <= to_date)
    total = q.count()
    items = q.order_by(HealthMarker.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.post("/", response_model=HealthMarkerRead, status_code=status.HTTP_201_CREATED)
def create_health_marker(data: HealthMarkerCreate, db: Session = Depends(get_db)):
    obj = HealthMarker(**data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{marker_id}", response_model=HealthMarkerRead)
def get_health_marker(marker_id: int, db: Session = Depends(get_db)):
    obj = db.get(HealthMarker, marker_id)
    if not obj:
        raise resource_not_found("HealthMarker", marker_id)
    return obj


@router.patch("/{marker_id}", response_model=HealthMarkerRead)
def update_health_marker(marker_id: int, data: HealthMarkerUpdate, db: Session = Depends(get_db)):
    obj = db.get(HealthMarker, marker_id)
    if not obj:
        raise resource_not_found("HealthMarker", marker_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{marker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_health_marker(marker_id: int, db: Session = Depends(get_db)):
    obj = db.get(HealthMarker, marker_id)
    if not obj:
        raise resource_not_found("HealthMarker", marker_id)
    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
