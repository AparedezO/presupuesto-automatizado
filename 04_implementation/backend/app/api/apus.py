from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.excel.workbook import FormulaIntegrityError, WorkbookLockedError
from app.schemas.apus import ApuCreate, ApuDraftRead, ApuRead
from app.services.apu_service import ApuService
from app.services.code_generator import generate_material_code


router = APIRouter(prefix="/apus", tags=["apus"])


class ApuSearchResponse(BaseModel):
    items: list[ApuRead]
    total: int
    search: str
    can_create: bool
    suggested_code: str | None = None


class ApuCreateResponse(BaseModel):
    header_row: int
    detail_rows: int
    backup_path: str
    formula_integrity_ok: bool


class ApuSuggestedCodeResponse(BaseModel):
    description: str
    suggested_code: str


def get_service() -> ApuService:
    return ApuService()


@router.get("", response_model=ApuSearchResponse)
def list_apus(
    search: str = Query(default=""),
    limit: int = Query(default=80, ge=1, le=500),
):
    service = get_service()
    items = service.search(search)
    limited_items = items[:limit]
    normalized_search = search.strip()
    exact_match = any(
        item.codigo_apu.upper() == normalized_search.upper()
        or item.descripcion_apu.upper() == normalized_search.upper()
        for item in items
    )

    return ApuSearchResponse(
        items=limited_items,
        total=len(items),
        search=normalized_search,
        can_create=bool(normalized_search) and not exact_match,
        suggested_code=generate_material_code(normalized_search, max_length=28)
        if normalized_search and not exact_match
        else None,
    )


@router.get("/suggest-code", response_model=ApuSuggestedCodeResponse)
def suggest_apu_code(description: str = Query(..., min_length=1)):
    return ApuSuggestedCodeResponse(
        description=description,
        suggested_code=generate_material_code(description, max_length=28),
    )


@router.get("/{row_number}/draft", response_model=ApuDraftRead)
def get_apu_draft(row_number: int):
    service = get_service()
    try:
        return service.draft_from_row(row_number)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=ApuCreateResponse, status_code=status.HTTP_201_CREATED)
def create_apu(payload: ApuCreate):
    service = get_service()
    try:
        result = service.create(payload)
        return ApuCreateResponse(**result)
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
