from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request


def resource_not_found(resource: str, id: int) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{resource} with id {id} not found")


def duplicate_entry(detail: str) -> HTTPException:
    return HTTPException(status_code=409, detail=detail)


async def handle_integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
    msg = str(exc.orig) if exc.orig else str(exc)

    if "unique" in msg.lower() or "duplicate" in msg.lower():
        return JSONResponse(status_code=409, content={"detail": f"Duplicate entry: {msg}"})

    if "check" in msg.lower():
        return JSONResponse(status_code=422, content={"detail": f"Constraint violation: {msg}"})

    if "foreign" in msg.lower() or "fk_" in msg.lower():
        return JSONResponse(status_code=422, content={"detail": f"Foreign key violation: {msg}"})

    return JSONResponse(status_code=400, content={"detail": f"Integrity error: {msg}"})
