from __future__ import annotations

from decimal import Decimal

from app.excel.formulas import collect_workbook_formulas
from app.excel.workbook import ExcelWorkbook, copy_row_format_and_formulas, find_last_data_row
from app.schemas.materials import MaterialCreate, MaterialRead


MATERIALS_SHEET = "L-MATERIALES"
HEADER_ROW = 4
FIRST_DATA_ROW = 5
CODE_COL = 2


def _decimal_or_zero(value) -> Decimal:
    if value in (None, ""):
        return Decimal("0")
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


class MaterialsRepository:
    def __init__(self, excel: ExcelWorkbook | None = None) -> None:
        self.excel = excel or ExcelWorkbook()

    def list_materials(self) -> list[MaterialRead]:
        workbook = self.excel.load()
        try:
            sheet = workbook[MATERIALS_SHEET]
            last_row = find_last_data_row(sheet, CODE_COL, FIRST_DATA_ROW)
            materials: list[MaterialRead] = []

            for row in range(FIRST_DATA_ROW, last_row + 1):
                code = sheet.cell(row=row, column=2).value
                if code in (None, ""):
                    continue
                materials.append(
                    MaterialRead(
                        row_number=row,
                        codigo=str(code).strip(),
                        descripcion=str(sheet.cell(row=row, column=3).value or "").strip(),
                        marca=sheet.cell(row=row, column=4).value,
                        und=str(sheet.cell(row=row, column=5).value or "").strip(),
                        factor=_decimal_or_zero(sheet.cell(row=row, column=6).value),
                        valor_costo_incluido_iva=_decimal_or_zero(
                            sheet.cell(row=row, column=7).value
                        ),
                        valor_presupuesto_formula=sheet.cell(row=row, column=8).value,
                    )
                )

            return materials
        finally:
            workbook.close()

    def exists(self, codigo: str) -> bool:
        target = codigo.strip().upper()
        return any(material.codigo.upper() == target for material in self.list_materials())

    def search(self, term: str) -> list[MaterialRead]:
        target = term.strip().upper()
        if not target:
            return self.list_materials()
        return [
            material
            for material in self.list_materials()
            if target in material.codigo.upper() or target in material.descripcion.upper()
        ]

    def add_material(self, material: MaterialCreate) -> dict:
        if self.exists(material.codigo):
            raise ValueError(f"Material code already exists: {material.codigo}")

        workbook = self.excel.load()
        try:
            before_formulas = collect_workbook_formulas(workbook)
            sheet = workbook[MATERIALS_SHEET]
            source_row = find_last_data_row(sheet, CODE_COL, FIRST_DATA_ROW)
            target_row = source_row + 1
            added_formulas = copy_row_format_and_formulas(sheet, source_row, target_row)

            sheet.cell(row=target_row, column=2).value = material.codigo.strip()
            sheet.cell(row=target_row, column=3).value = material.descripcion.strip()
            sheet.cell(row=target_row, column=4).value = material.marca
            sheet.cell(row=target_row, column=5).value = material.und.strip()
            sheet.cell(row=target_row, column=6).value = float(material.factor)
            sheet.cell(row=target_row, column=7).value = float(material.valor_costo_incluido_iva)

            backup_path, report = self.excel.save_preserving_formulas(
                workbook,
                before_formulas,
                allowed_added_formulas=added_formulas,
            )

            return {
                "row_number": target_row,
                "backup_path": str(backup_path),
                "added_formulas": len(added_formulas),
                "formula_integrity_ok": report.ok,
            }
        finally:
            workbook.close()
