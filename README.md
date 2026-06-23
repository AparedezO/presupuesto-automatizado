# Presupuesto Automatizado 2.0

Aplicación local para gestionar materiales, APUs y presupuestos eléctricos usando el libro Excel `PRESUPUESTO-TULUA2.xlsx` como fuente de verdad.

## Estado

Versión funcional local alineada con `SPEC-001`.

Incluye:

- Búsqueda y creación de materiales.
- Búsqueda y creación de APUs.
- APUs nuevos con materiales, filas estándar y fila final en blanco.
- Módulo de presupuesto con guardado en hoja nueva.
- Preservación de fórmulas, formatos y backups del Excel.
- Frontend responsive con colores institucionales.

## Estructura SDD

- `PROJECT_CONTEXT.md`: contexto ejecutivo del proyecto.
- `01_sdd/02_specs/spec.md`: especificación funcional principal.
- `01_sdd/05_traceability/TRACEABILITY_MATRIX.md`: trazabilidad requisito-código-prueba.
- `02_design/architecture/ARCHITECTURE.md`: arquitectura técnica.
- `02_design/decisions/ADR-001-excel-write-engine.md`: decisión del motor Excel.
- `03_planning/tasks/TASK-001-modulos-materiales-apus-presupuesto.md`: tarea implementada.
- `05_validation/test_plans/VALIDATION_PLAN.md`: plan de validación.
- `05_validation/evidence/VALIDATION_REPORT.md`: evidencia de validación.
- `06_delivery/RUNBOOK.md`: guía de ejecución local.

## Ejecutar En VS Code

Abrir la carpeta:

```text
D:\PROGRAMACION\04_Presupuesto Automatizado 2.0
```

Backend:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Frontend:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run dev -- --host 127.0.0.1 --port 5173
```

Abrir:

```text
http://127.0.0.1:5173
```

## Validar

Backend:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m pytest -q
```

Frontend:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run build
```

## Nota Operativa

Cerrar `04_implementation/data/PRESUPUESTO-TULUA2.xlsx` antes de guardar desde la app. Si Excel lo mantiene abierto, Windows puede bloquear la escritura.
