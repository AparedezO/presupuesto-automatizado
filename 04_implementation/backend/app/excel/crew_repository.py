from __future__ import annotations

from decimal import Decimal

from app.excel.workbook import ExcelWorkbook
from app.schemas.crew import CrewRead


LABOR_SHEET = "MANO DE OBRA"
CREW_START_ROW = 3
CREW_END_ROW = 7


def _decimal_or_zero(value) -> Decimal:
    if value in (None, ""):
        return Decimal("0")
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


class CrewRepository:
    def __init__(self, excel: ExcelWorkbook | None = None) -> None:
        self.excel = excel or ExcelWorkbook()

    def list_crew(self) -> list[CrewRead]:
        workbook = self.excel.load()
        try:
            sheet = workbook[LABOR_SHEET]
            items: list[CrewRead] = []
            for row in range(CREW_START_ROW, CREW_END_ROW + 1):
                code = sheet.cell(row=row, column=1).value
                description = sheet.cell(row=row, column=1).value
                if code in (None, ""):
                    continue
                items.append(
                    CrewRead(
                        row_number=row,
                        codigo=str(code).strip(),
                        descripcion=str(description or "").strip(),
                        valor_dia=_decimal_or_zero(sheet.cell(row=row, column=5).value),
                        disponibilidad=_decimal_or_zero(sheet.cell(row=row, column=6).value),
                        valor_hora_formula=sheet.cell(row=row, column=7).value,
                    )
                )
            return items
        finally:
            workbook.close()

    def search(self, term: str) -> list[CrewRead]:
        target = term.strip().upper()
        if not target:
            return self.list_crew()
        return [
            item
            for item in self.list_crew()
            if target in item.codigo.upper() or target in item.descripcion.upper()
        ]
