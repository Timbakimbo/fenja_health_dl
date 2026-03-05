from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload

from fenja_health_dl.auth import verify_api_key
from fenja_health_dl.db import get_db
from fenja_health_dl.errors import resource_not_found
from fenja_health_dl.models import VetVisit
from fenja_health_dl.schemas.pagination import DEFAULT_PAGE_SIZE, PaginatedResponse, clamp_page_size
from fenja_health_dl.schemas.vet_visit import VetVisitCreate, VetVisitRead, VetVisitUpdate

router = APIRouter(
    prefix="/api/vet-visits",
    tags=["vet-visits"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/", response_model=PaginatedResponse[VetVisitRead])
def list_vet_visits(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_db),
):
    page_size = clamp_page_size(page_size)
    q = db.query(VetVisit).options(joinedload(VetVisit.protocols))
    if from_date:
        q = q.filter(VetVisit.timestamp >= from_date)
    if to_date:
        q = q.filter(VetVisit.timestamp <= to_date)
    # Use subquery for count to avoid counting joined rows
    count_q = db.query(VetVisit)
    if from_date:
        count_q = count_q.filter(VetVisit.timestamp >= from_date)
    if to_date:
        count_q = count_q.filter(VetVisit.timestamp <= to_date)
    total = count_q.count()
    items = q.order_by(VetVisit.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
    # Deduplicate due to joinedload
    seen = set()
    unique_items = []
    for item in items:
        if item.id not in seen:
            seen.add(item.id)
            unique_items.append(item)
    return PaginatedResponse.create(items=unique_items, total=total, page=page, page_size=page_size)


@router.post("/", response_model=VetVisitRead, status_code=status.HTTP_201_CREATED)
def create_vet_visit(data: VetVisitCreate, db: Session = Depends(get_db)):
    obj = VetVisit(**data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{visit_id}", response_model=VetVisitRead)
def get_vet_visit(visit_id: int, db: Session = Depends(get_db)):
    obj = db.get(VetVisit, visit_id)
    if not obj:
        raise resource_not_found("VetVisit", visit_id)
    return obj


@router.patch("/{visit_id}", response_model=VetVisitRead)
def update_vet_visit(visit_id: int, data: VetVisitUpdate, db: Session = Depends(get_db)):
    obj = db.get(VetVisit, visit_id)
    if not obj:
        raise resource_not_found("VetVisit", visit_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vet_visit(visit_id: int, db: Session = Depends(get_db)):
    obj = db.get(VetVisit, visit_id)
    if not obj:
        raise resource_not_found("VetVisit", visit_id)
    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
