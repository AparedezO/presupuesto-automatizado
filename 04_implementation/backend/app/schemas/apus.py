from __future__ import annotations

from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, Field


ItemType = Literal["MATERIAL", "LABOR", "CUADRILLA"]


class ApuDetail(BaseModel):
    tipo_item: ItemType
    codigo_item: str = Field(..., min_length=1)
    cantidad: Decimal | str = Decimal("1")
    source_row_number: Optional[int] = None
    cantidad_formula: Optional[str] = None


class ApuHeader(BaseModel):
    codigo_apu: str = Field(..., min_length=1)
    descripcion_apu: str = Field(..., min_length=1)
    unidad: str = Field(..., min_length=1)


class ApuRead(ApuHeader):
    row_number: int
    costo_total_formula: Optional[str] = None


class ApuCreate(ApuHeader):
    detalles: list[ApuDetail] = Field(default_factory=list)


class ApuDraftDetail(BaseModel):
    row_number: int
    source_row_number: int
    tipo_item: ItemType
    codigo_item: str = Field(..., min_length=1)
    cantidad: str = "1"
    cantidad_formula: Optional[str] = None
    descripcion: Optional[str] = None
    und: Optional[str] = None
    costo: Optional[str] = None


class ApuDraftRead(BaseModel):
    base_row_number: int
    base_codigo_apu: str
    codigo_apu: str = ""
    descripcion_apu: str = Field(..., min_length=1)
    unidad: str = Field(..., min_length=1)
    detalles: list[ApuDraftDetail] = Field(default_factory=list)
