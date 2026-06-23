from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.excel.budget_repository import BudgetRepository
from app.excel.workbook import FormulaIntegrityError, WorkbookLockedError
from app.schemas.budget import (
    BudgetAddResponse,
    BudgetApuCreate,
    BudgetExportRequest,
    BudgetExportResponse,
    BudgetItemRead,
    BudgetSaveRequest,
    BudgetSaveResponse,
)


router = APIRouter(prefix="/budget", tags=["budget"])


class BudgetListResponse(BaseModel):
    items: list[BudgetItemRead]
    total: int


def get_repository() -> BudgetRepository:
    return BudgetRepository()


@router.get("", response_model=BudgetListResponse)
def list_budget_items():
    repository = get_repository()
    items = repository.list_items()
    return BudgetListResponse(items=items, total=len(items))


@router.post("/apus", response_model=BudgetAddResponse, status_code=status.HTTP_201_CREATED)
def add_apu_to_budget(payload: BudgetApuCreate):
    repository = get_repository()
    try:
        result = repository.add_apu(payload)
        return BudgetAddResponse(**result)
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


@router.post("/save", response_model=BudgetSaveResponse, status_code=status.HTTP_201_CREATED)
def save_budget(payload: BudgetSaveRequest):
    repository = get_repository()
    try:
        result = repository.save_budget(payload.items, payload.sheet_name)
        return BudgetSaveResponse(**result)
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


@router.post("/export", response_model=BudgetExportResponse, status_code=status.HTTP_201_CREATED)
def export_filtered_budget(payload: BudgetExportRequest):
    repository = get_repository()
    try:
        result = repository.export_filtered_budget(
            items=payload.items,
            export_code=payload.export_code,
            sheet_name=payload.sheet_name,
        )
        return BudgetExportResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except WorkbookLockedError as exc:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="El archivo Excel esta abierto o bloqueado. Cierra Excel e intenta de nuevo.",
        ) from exc
