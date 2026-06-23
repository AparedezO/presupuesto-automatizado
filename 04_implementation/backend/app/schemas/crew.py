from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class CrewRead(BaseModel):
    row_number: int
    codigo: str
    descripcion: str
    valor_dia: Decimal
    disponibilidad: Decimal | None = None
    valor_hora_formula: str | None = None
