from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class LaborCreate(BaseModel):
    codigo: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    valor_dia: Decimal = Decimal("0")
    und: str = Field(default="HR", min_length=1)


class LaborRead(LaborCreate):
    row_number: int
    valor_hora_formula: str | None = None
