from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.excel.workbook import FormulaIntegrityError, WorkbookLockedError
from app.schemas.labor import LaborCreate, LaborRead
from app.services.labor_service import LaborService


router = APIRouter(prefix="/labor", tags=["labor"])


class LaborSearchResponse(BaseModel):
    items: list[LaborRead]
    total: int
    search: str
    can_create: bool


class LaborCreateResponse(BaseModel):
    row_number: int
    formula_snapshot_size: int


def get_service() -> LaborService:
    return LaborService()


@router.get("", response_model=LaborSearchResponse)
def search_labor(
    search: str = Query(default=""),
    limit: int = Query(default=80, ge=1, le=500),
):
    service = get_service()
    items = service.search(search)
    limited_items = items[:limit]
    normalized_search = search.strip()
    exact_match = any(
        item.codigo.upper() == normalized_search.upper()
        or item.descripcion.upper() == normalized_search.upper()
        for item in items
    )

    return LaborSearchResponse(
        items=limited_items,
        total=len(items),
        search=normalized_search,
        can_create=bool(normalized_search) and not exact_match,
    )


@router.post("", response_model=LaborCreateResponse, status_code=status.HTTP_201_CREATED)
def create_labor(payload: LaborCreate):
    service = get_service()
    try:
        result = service.create(payload)
        return LaborCreateResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except WorkbookLockedError as exc:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="El archivo Excel esta abierto o bloqueado. Cierra Excel e intenta de nuevo.",
        ) from exc
    except FormulaIntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "La verificacion de formulas fallo. No se guardaron cambios.",
                "changed": exc.report.changed,
                "removed": exc.report.removed,
            },
        ) from exc
