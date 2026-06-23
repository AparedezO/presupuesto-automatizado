from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class MaterialCreate(BaseModel):
    codigo: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    marca: Optional[str] = None
    und: str = Field(..., min_length=1)
    factor: Decimal = Decimal("0")
    valor_costo_incluido_iva: Decimal = Decimal("0")


class MaterialRead(MaterialCreate):
    row_number: int
    valor_presupuesto_formula: Optional[str] = None
