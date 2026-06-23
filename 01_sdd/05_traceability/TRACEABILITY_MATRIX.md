# Matriz De Trazabilidad

## Resumen

Esta matriz conecta necesidades, requisitos SDD, implementación y pruebas para mantener el proyecto gobernado por especificación.

| ID | Necesidad | Spec | Implementación | Prueba / Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| MAT-001 | Buscar materiales por código o descripción | `SPEC-001` sección 5 | `04_implementation/backend/app/api/materials.py`, `04_implementation/frontend/src/features/materials/MaterialsPage.tsx` | `test_can_read_materials_and_apus` | Implementado |
| MAT-002 | Crear materiales sin romper fórmulas | `SPEC-001` sección 5 | `04_implementation/backend/app/excel/materials_repository.py`, `04_implementation/frontend/src/features/materials/CreateMaterialDialog.tsx` | `test_add_material_on_copy_preserves_existing_formulas` | Implementado |
| MAT-003 | Sugerir código inteligente de material | `SPEC-001` sección 5 | `04_implementation/backend/app/services/code_generator.py`, `04_implementation/backend/app/services/materials_service.py` | `test_material_service_suggests_unique_code` | Implementado |
| APU-001 | Buscar APUs existentes | `SPEC-001` sección 5 | `04_implementation/backend/app/api/apus.py`, `04_implementation/frontend/src/features/apus/ApusPage.tsx` | `test_can_read_materials_and_apus` | Implementado |
| APU-002 | Crear APU con materiales desde la app | `SPEC-001` sección 5 | `04_implementation/backend/app/excel/apu_repository.py`, `04_implementation/frontend/src/features/apus/ApusPage.tsx` | `test_create_apu_adds_standard_formula_rows` | Implementado |
| APU-003 | Cerrar APU con filas estándar y fila en blanco | `SPEC-001` sección 5 | `04_implementation/backend/app/excel/apu_repository.py` | `test_create_apu_adds_standard_formula_rows` | Implementado |
| APU-004 | Editar como nuevo desde un APU similar | `SPEC-001` sección 5 | `04_implementation/backend/app/api/apus.py`, `04_implementation/backend/app/excel/apu_repository.py`, `04_implementation/frontend/src/features/apus/ApusPage.tsx`, `04_implementation/frontend/src/store/apuBuilderStore.ts` | `test_get_apu_draft_from_existing_row_returns_materials_only`, `test_apu_draft_endpoint_returns_base_materials` | Implementado |
| PRE-001 | Agregar APUs a presupuesto temporal | `SPEC-001` sección 5 | `04_implementation/backend/app/api/budget.py`, `04_implementation/frontend/src/features/budget/BudgetPage.tsx`, `04_implementation/frontend/src/store/budgetStore.ts` | Prueba manual + API budget | Implementado |
| PRE-002 | Guardar presupuesto en hoja nueva con formato del modelo | `SPEC-001` sección 5 | `04_implementation/backend/app/excel/budget_repository.py` | `test_save_budget_creates_new_sheet_with_template_columns_and_formulas` | Implementado |
| PRE-003 | Exportar archivo nuevo filtrado por presupuesto | `SPEC-001` sección 5 | `04_implementation/backend/app/api/budget.py`, `04_implementation/backend/app/excel/budget_repository.py`, `04_implementation/frontend/src/features/budget/BudgetPage.tsx` | `test_export_filtered_budget_creates_workbook_with_only_used_apus_and_materials` | Implementado |
| UI-001 | Aplicar identidad visual institucional | `SPEC-001` sección 5 | `04_implementation/frontend/src/styles/main.css` | `npm run build` | Implementado |
| NFR-001 | Preservar fórmulas existentes | `SPEC-001` sección 6 | `04_implementation/backend/app/excel/workbook.py`, `04_implementation/backend/app/excel/formulas.py` | Pruebas de integridad Excel | Implementado |
| NFR-002 | Crear backup antes de guardar | `SPEC-001` sección 6 | `04_implementation/backend/app/excel/backups.py`, repositorios Excel | Pruebas de escritura Excel | Implementado |
| NFR-003 | Ejecución local backend/frontend | `SPEC-001` sección 6 | `04_implementation/backend/app/main.py`, `04_implementation/frontend/package.json` | `GET /health`, Vite dev server | Implementado |

## Reglas De Mantenimiento

- Todo cambio funcional nuevo debe agregar o actualizar una fila de esta matriz.
- Si un requisito cambia, actualizar primero `01_sdd/02_specs/spec.md`.
- Si se agrega una decisión técnica, crear un ADR en `02_design/decisions`.
- Si se agrega una prueba manual relevante, registrar evidencia en `05_validation/evidence`.
