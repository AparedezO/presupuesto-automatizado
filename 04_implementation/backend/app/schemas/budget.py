from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class BudgetApuCreate(BaseModel):
    codigo_apu: str = Field(..., min_length=1)
    cantidad: Decimal = Decimal("1")


class BudgetItemRead(BaseModel):
    row_number: int
    item: int
    codigo_apu: str
    descripcion_apu: str
    unidad: str
    cantidad: Decimal
    material_formula: Optional[str] = None
    mano_obra_formula: Optional[str] = None
    valor_unitario_formula: Optional[str] = None
    valor_total_formula: Optional[str] = None


class BudgetAddResponse(BaseModel):
    item: BudgetItemRead
    row_number: int
    backup_path: str
    formula_integrity_ok: bool


class BudgetSaveRequest(BaseModel):
    items: list[BudgetApuCreate] = Field(..., min_length=1)
    sheet_name: str = "PRESUPUESTO"


class BudgetSaveResponse(BaseModel):
    sheet_name: str
    rows: int
    backup_path: str
    formula_integrity_ok: bool


class BudgetExportRequest(BudgetSaveRequest):
    export_code: str = Field(..., min_length=1, max_length=80)


class BudgetExportResponse(BaseModel):
    file_name: str
    file_path: str
    sheet_name: str
    rows: int
    apus: int
    materials: int
