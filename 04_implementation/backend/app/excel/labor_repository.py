from __future__ import annotations

from decimal import Decimal

from app.excel.formulas import collect_workbook_formulas
from app.excel.workbook import ExcelWorkbook, copy_row_format_and_formulas
from app.schemas.labor import LaborCreate, LaborRead


LABOR_SHEET = "MANO DE OBRA"
EQUIPMENT_START_ROW = 3
EQUIPMENT_END_ROW = 13
CODE_COL = 9
DESCRIPTION_COL = 10
VALUE_COL = 12
UNIT_COL = 13
HOUR_COL = 14


def _decimal_or_zero(value) -> Decimal:
    if value in (None, ""):
        return Decimal("0")
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def _hour_formula_for_unit(unit: str, row_number: int) -> str:
    normalized = unit.strip().upper()
    if normalized in {"HR", "HORA", "HORAS"}:
        return f"=+L{row_number}/8"
    return f"=+L{row_number}"


class LaborRepository:
    def __init__(self, excel: ExcelWorkbook | None = None) -> None:
        self.excel = excel or ExcelWorkbook()

    def _find_equipment_row(self, sheet) -> int | None:
        for row in range(EQUIPMENT_START_ROW, EQUIPMENT_END_ROW + 1):
            if sheet.cell(row=row, column=CODE_COL).value in (None, ""):
                return row
        return None

    def list_equipment(self) -> list[LaborRead]:
        workbook = self.excel.load()
        try:
            sheet = workbook[LABOR_SHEET]
            items: list[LaborRead] = []
            for row in range(EQUIPMENT_START_ROW, EQUIPMENT_END_ROW + 1):
                code = sheet.cell(row=row, column=CODE_COL).value
                description = sheet.cell(row=row, column=DESCRIPTION_COL).value
                if code in (None, "") or description in (None, ""):
                    continue
                items.append(
                    LaborRead(
                        row_number=row,
                        codigo=str(code).strip(),
                        descripcion=str(description).strip(),
                        valor_dia=_decimal_or_zero(sheet.cell(row=row, column=VALUE_COL).value),
                        und=str(sheet.cell(row=row, column=UNIT_COL).value or "").strip(),
                        valor_hora_formula=sheet.cell(row=row, column=HOUR_COL).value,
                    )
                )
            return items
        finally:
            workbook.close()

    def search(self, term: str) -> list[LaborRead]:
        target = term.strip().upper()
        if not target:
            return self.list_equipment()
        return [
            item
            for item in self.list_equipment()
            if target in item.codigo.upper() or target in item.descripcion.upper()
        ]

    def exists(self, codigo: str) -> bool:
        target = codigo.strip().upper()
        return any(item.codigo.upper() == target for item in self.list_equipment())

    def add_equipment(self, labor: LaborCreate) -> dict:
        if self.exists(labor.codigo):
            raise ValueError(f"Labor code already exists: {labor.codigo}")

        workbook = self.excel.load()
        try:
            before_formulas = collect_workbook_formulas(workbook)
            sheet = workbook[LABOR_SHEET]
            target_row = self._find_equipment_row(sheet)
            if target_row is None:
                raise ValueError(
                    "No hay filas libres para crear mas mano de obra/equipo en la seccion disponible."
                )

            source_row = EQUIPMENT_END_ROW
            copy_row_format_and_formulas(sheet, source_row, target_row)

            sheet.cell(row=target_row, column=CODE_COL).value = labor.codigo.strip()
            sheet.cell(row=target_row, column=DESCRIPTION_COL).value = labor.descripcion.strip()
            sheet.cell(row=target_row, column=VALUE_COL).value = float(labor.valor_dia)
            sheet.cell(row=target_row, column=UNIT_COL).value = labor.und.strip()
            sheet.cell(row=target_row, column=HOUR_COL).value = _hour_formula_for_unit(
                labor.und, target_row
            )

            return {
                "row_number": target_row,
                "formula_snapshot_size": len(before_formulas),
            }
        finally:
            workbook.close()
