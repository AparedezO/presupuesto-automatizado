# Presupuesto Automatizado 2.0

## Propósito

Construir una aplicación local para automatizar la consulta, creación y armado de presupuestos eléctricos usando como fuente principal el libro Excel `PRESUPUESTO-TULUA2.xlsx`.

El sistema debe facilitar el trabajo diario sin reemplazar la lógica financiera existente del archivo: las fórmulas, formatos, rangos nombrados y vínculos entre hojas se consideran parte crítica del producto.

## Método De Trabajo

Este proyecto se gestiona con Spec Driven Development (SDD):

1. Registrar necesidad o cambio solicitado.
2. Actualizar la especificación antes de implementar cambios funcionales.
3. Diseñar la solución técnica mínima.
4. Implementar en backend, frontend y/o Excel.
5. Validar contra criterios de aceptación y pruebas automatizadas.
6. Actualizar trazabilidad, tareas y documentación de entrega.

## Regla Principal

Ninguna funcionalidad importante debe implementarse sin quedar trazada en la especificación, con criterio de aceptación y evidencia de validación.

## Estado Actual

Versión funcional local con:

- Backend FastAPI que lee y escribe el libro Excel preservando fórmulas existentes.
- Frontend React/Vite responsive con módulos de Materiales, APUs y Presupuesto.
- Creación de materiales con sugerencia de código y preservación de fórmulas.
- Creación de APUs solo con materiales manuales, filas estándar `E&H`, `GLV`, `T`, `H/C` y fila final en blanco con fórmula en columna A.
- Presupuesto editable desde la app y guardado en nueva hoja Excel basada en `PRESUPUESTO UNIFORCE`.
- Estilo visual institucional: rojo `rgb(192, 0, 0)`, gris `rgb(217, 217, 217)`, blanco y textos normales en negro.

## Fuente De Datos

- Libro principal: `04_implementation/data/PRESUPUESTO-TULUA2.xlsx`
- Hojas críticas: `L-MATERIALES`, `APU'S`, `PRESUPUESTO UNIFORCE`, `MANO DE OBRA`, `CUADRILLA`
- Backups automáticos: `04_implementation/data/backups`

## Comandos Principales

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

Aplicación:

```text
http://127.0.0.1:5173
```
