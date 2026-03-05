from datetime import date

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from fenja_health_dl.auth import verify_api_key
from fenja_health_dl.db import get_db
from fenja_health_dl.errors import resource_not_found
from fenja_health_dl.models import TreatmentEntry, TreatmentProtocol, TreatmentTemplate
from fenja_health_dl.schemas.pagination import DEFAULT_PAGE_SIZE, PaginatedResponse, clamp_page_size
from fenja_health_dl.schemas.treatment import (
    TreatmentEntryCreate,
    TreatmentEntryRead,
    TreatmentEntryUpdate,
    TreatmentProtocolCreate,
    TreatmentProtocolRead,
    TreatmentProtocolUpdate,
    TreatmentTemplateCreate,
    TreatmentTemplateRead,
    TreatmentTemplateUpdate,
)

# --- Templates Router ---

templates_router = APIRouter(
    prefix="/api/treatment-templates",
    tags=["treatment-templates"],
    dependencies=[Depends(verify_api_key)],
)


@templates_router.get("/", response_model=PaginatedResponse[TreatmentTemplateRead])
def list_templates(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    category: str | None = None,
    db: Session = Depends(get_db),
):
    page_size = clamp_page_size(page_size)
    q = db.query(TreatmentTemplate)
    if category:
        q = q.filter(TreatmentTemplate.category == category)
    total = q.count()
    items = q.order_by(TreatmentTemplate.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@templates_router.post("/", response_model=TreatmentTemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(data: TreatmentTemplateCreate, db: Session = Depends(get_db)):
    obj = TreatmentTemplate(**data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@templates_router.get("/{template_id}", response_model=TreatmentTemplateRead)
def get_template(template_id: int, db: Session = Depends(get_db)):
    obj = db.get(TreatmentTemplate, template_id)
    if not obj:
        raise resource_not_found("TreatmentTemplate", template_id)
    return obj


@templates_router.patch("/{template_id}", response_model=TreatmentTemplateRead)
def update_template(template_id: int, data: TreatmentTemplateUpdate, db: Session = Depends(get_db)):
    obj = db.get(TreatmentTemplate, template_id)
    if not obj:
        raise resource_not_found("TreatmentTemplate", template_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@templates_router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    obj = db.get(TreatmentTemplate, template_id)
    if not obj:
        raise resource_not_found("TreatmentTemplate", template_id)
    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Protocols Router ---

protocols_router = APIRouter(
    prefix="/api/treatment-protocols",
    tags=["treatment-protocols"],
    dependencies=[Depends(verify_api_key)],
)


def _get_protocol_or_404(protocol_id: int, db: Session) -> TreatmentProtocol:
    obj = db.get(TreatmentProtocol, protocol_id)
    if not obj:
        raise resource_not_found("TreatmentProtocol", protocol_id)
    return obj


@protocols_router.get("/", response_model=PaginatedResponse[TreatmentProtocolRead])
def list_protocols(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    active: bool | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    page_size = clamp_page_size(page_size)
    q = db.query(TreatmentProtocol)
    if active is not None:
        q = q.filter(TreatmentProtocol.active == active)
    if category:
        q = q.filter(TreatmentProtocol.category == category)
    total = q.count()
    items = q.order_by(TreatmentProtocol.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@protocols_router.post("/", response_model=TreatmentProtocolRead, status_code=status.HTTP_201_CREATED)
def create_protocol(data: TreatmentProtocolCreate, db: Session = Depends(get_db)):
    obj = TreatmentProtocol(**data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@protocols_router.get("/{protocol_id}", response_model=TreatmentProtocolRead)
def get_protocol(protocol_id: int, db: Session = Depends(get_db)):
    return _get_protocol_or_404(protocol_id, db)


@protocols_router.patch("/{protocol_id}", response_model=TreatmentProtocolRead)
def update_protocol(protocol_id: int, data: TreatmentProtocolUpdate, db: Session = Depends(get_db)):
    obj = _get_protocol_or_404(protocol_id, db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@protocols_router.delete("/{protocol_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_protocol(protocol_id: int, db: Session = Depends(get_db)):
    obj = _get_protocol_or_404(protocol_id, db)
    db.delete(obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Nested Entries ---

def _get_entry_or_404(protocol_id: int, entry_id: int, db: Session) -> TreatmentEntry:
    entry = db.query(TreatmentEntry).filter(
        TreatmentEntry.id == entry_id,
        TreatmentEntry.protocol_id == protocol_id,
    ).first()
    if not entry:
        raise resource_not_found("TreatmentEntry", entry_id)
    return entry


@protocols_router.get("/{protocol_id}/entries", response_model=PaginatedResponse[TreatmentEntryRead])
def list_entries(
    protocol_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    from_date: date | None = None,
    to_date: date | None = None,
    skipped_only: bool = False,
    db: Session = Depends(get_db),
):
    _get_protocol_or_404(protocol_id, db)
    page_size = clamp_page_size(page_size)
    q = db.query(TreatmentEntry).filter(TreatmentEntry.protocol_id == protocol_id)
    if from_date:
        q = q.filter(TreatmentEntry.scheduled_date >= from_date)
    if to_date:
        q = q.filter(TreatmentEntry.scheduled_date <= to_date)
    if skipped_only:
        from datetime import date as date_type
        q = q.filter(
            TreatmentEntry.administered_at.is_(None),
            TreatmentEntry.scheduled_date < date_type.today(),
        )
    total = q.count()
    items = q.order_by(TreatmentEntry.scheduled_date.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@protocols_router.post("/{protocol_id}/entries", response_model=TreatmentEntryRead, status_code=status.HTTP_201_CREATED)
def create_entry(protocol_id: int, data: TreatmentEntryCreate, db: Session = Depends(get_db)):
    _get_protocol_or_404(protocol_id, db)
    obj = TreatmentEntry(protocol_id=protocol_id, **data.model_dump(exclude_unset=True))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@protocols_router.get("/{protocol_id}/entries/{entry_id}", response_model=TreatmentEntryRead)
def get_entry(protocol_id: int, entry_id: int, db: Session = Depends(get_db)):
    return _get_entry_or_404(protocol_id, entry_id, db)


@protocols_router.patch("/{protocol_id}/entries/{entry_id}", response_model=TreatmentEntryRead)
def update_entry(protocol_id: int, entry_id: int, data: TreatmentEntryUpdate, db: Session = Depends(get_db)):
    entry = _get_entry_or_404(protocol_id, entry_id, db)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


@protocols_router.delete("/{protocol_id}/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(protocol_id: int, entry_id: int, db: Session = Depends(get_db)):
    entry = _get_entry_or_404(protocol_id, entry_id, db)
    db.delete(entry)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
