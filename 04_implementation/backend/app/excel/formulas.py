from __future__ import annotations

from dataclasses import dataclass, field

from openpyxl.worksheet.worksheet import Worksheet


FormulaSnapshot = dict[str, str]


@dataclass(frozen=True)
class FormulaIntegrityReport:
    changed: dict[str, tuple[str, str]] = field(default_factory=dict)
    removed: dict[str, str] = field(default_factory=dict)
    added: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.changed and not self.removed


def collect_formulas(sheet: Worksheet) -> FormulaSnapshot:
    formulas: FormulaSnapshot = {}
    for row in sheet.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and cell.value.startswith("="):
                formulas[f"{sheet.title}!{cell.coordinate}"] = cell.value
    return formulas


def collect_workbook_formulas(workbook) -> FormulaSnapshot:
    formulas: FormulaSnapshot = {}
    for sheet in workbook.worksheets:
        formulas.update(collect_formulas(sheet))
    return formulas


def compare_formulas(
    before: FormulaSnapshot,
    after: FormulaSnapshot,
    allowed_added: set[str] | None = None,
) -> FormulaIntegrityReport:
    allowed_added = allowed_added or set()
    changed: dict[str, tuple[str, str]] = {}
    removed: dict[str, str] = {}
    added: dict[str, str] = {}

    for coordinate, old_formula in before.items():
        new_formula = after.get(coordinate)
        if new_formula is None:
            removed[coordinate] = old_formula
        elif new_formula != old_formula:
            changed[coordinate] = (old_formula, new_formula)

    for coordinate, new_formula in after.items():
        if coordinate not in before and coordinate not in allowed_added:
            added[coordinate] = new_formula

    return FormulaIntegrityReport(changed=changed, removed=removed, added=added)
