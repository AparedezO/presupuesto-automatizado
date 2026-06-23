from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.excel.workbook import FormulaIntegrityError, WorkbookLockedError
from app.schemas.materials import MaterialCreate, MaterialRead
from app.services.materials_service import MaterialsService


router = APIRouter(prefix="/materials", tags=["materials"])


class MaterialsSearchResponse(BaseModel):
    items: list[MaterialRead]
    total: int
    search: str
    can_create: bool
    suggested_code: str | None = None


class SuggestedCodeResponse(BaseModel):
    description: str
    suggested_code: str


class MaterialCreateResponse(BaseModel):
    material: MaterialRead
    row_number: int
    backup_path: str
    added_formulas: int
    formula_integrity_ok: bool


def get_service() -> MaterialsService:
    return MaterialsService()


@router.get("", response_model=MaterialsSearchResponse)
def list_materials(
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

    return MaterialsSearchResponse(
        items=limited_items,
        total=len(items),
        search=normalized_search,
        can_create=bool(normalized_search) and not exact_match,
        suggested_code=service.suggest_code(normalized_search)
        if normalized_search and not exact_match
        else None,
    )


@router.get("/suggest-code", response_model=SuggestedCodeResponse)
def suggest_material_code(description: str = Query(..., min_length=1)):
    service = get_service()
    return SuggestedCodeResponse(
        description=description,
        suggested_code=service.suggest_code(description),
    )


@router.post("", response_model=MaterialCreateResponse, status_code=status.HTTP_201_CREATED)
def create_material(payload: MaterialCreate):
    service = get_service()
    try:
        result = service.create(payload)
        material = next(
            item
            for item in service.search(payload.codigo)
            if item.codigo.upper() == payload.codigo.upper()
        )
        return MaterialCreateResponse(material=material, **result)
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
