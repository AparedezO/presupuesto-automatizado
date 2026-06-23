# Reporte De Validación

## Fecha

2026-06-03

## Versión Validada

Implementación local de `SPEC-001 - Gestor De Presupuestos APU`.

## Comandos Ejecutados

Backend:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m pytest -q
```

Resultado:

```text
16 passed
```

Frontend:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run build
```

Resultado:

```text
vite build completado correctamente
```

## Evidencia Funcional

- `GET /health` responde `{"status":"ok"}`.
- `GET /api/materials` responde datos del Excel.
- `GET /api/apus` responde datos del Excel.
- Pruebas de integridad confirman que crear materiales preserva fórmulas existentes.
- Pruebas de integridad confirman que crear APU agrega filas estándar y fila final en blanco.
- Pruebas confirman que `Editar como nuevo` carga materiales del APU base sin incluir filas estándar.
- Pruebas confirman que cantidades con fórmula se muestran como valor numérico, conservan la fórmula internamente y se trasladan al nuevo APU con referencias ajustadas si no se editan.
- Pruebas de integridad confirman que guardar presupuesto crea hoja nueva con bloque final dinámico.
- Pruebas confirman que la exportación filtrada crea un archivo nuevo con `PRESUPUESTO`, APUs usados y materiales usados.

## Observaciones

- `openpyxl` escribe fórmulas, pero no calcula valores; Microsoft Excel recalcula al abrir el archivo.
- El archivo Excel debe estar cerrado para que la app pueda guardar.
- Si el usuario cambia filas modelo en Excel, se deben revisar las constantes de plantilla de los repositorios.
