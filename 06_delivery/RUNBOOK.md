# Guía De Ejecución Local

## Requisitos

- Windows.
- VS Code.
- PowerShell.
- Python virtualenv ya creado en `04_implementation/backend/.venv`.
- Dependencias frontend instaladas en `04_implementation/frontend/node_modules`.
- El archivo Excel `PRESUPUESTO-TULUA2.xlsx` debe estar cerrado al guardar cambios desde la app.

## Abrir Proyecto

Abrir en VS Code la carpeta raíz:

```text
D:\PROGRAMACION\04_Presupuesto Automatizado 2.0
```

## Ejecutar Backend

Abrir una terminal PowerShell:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Verificación:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health
```

Respuesta esperada:

```json
{"status":"ok"}
```

## Ejecutar Frontend

Abrir una segunda terminal PowerShell:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run dev -- --host 127.0.0.1 --port 5173
```

Abrir la aplicación:

```powershell
start chrome "http://127.0.0.1:5173"
```

## Validar API

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/materials
Invoke-WebRequest http://127.0.0.1:8000/api/apus
```

Si el frontend muestra `Failed to fetch`, revisar:

- Que el backend siga corriendo en `127.0.0.1:8000`.
- Que el frontend esté abierto desde `127.0.0.1:5173`.
- Que no haya otro proceso ocupando los puertos.
- Que el firewall no haya bloqueado Python o Node.

## Detener Puertos

Si necesitas liberar puertos:

```powershell
netstat -ano | Select-String ":8000\s|:5173\s"
```

Luego cerrar las terminales o finalizar el proceso correspondiente desde el Administrador de tareas.

## Ejecutar Pruebas Backend

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m pytest -q
```

Resultado esperado:

```text
10 passed
```

## Build Frontend

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run build
```

## Problemas Frecuentes

### El navegador dice `Failed to fetch`

El frontend no logra conectarse al backend. Ejecutar:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health
```

Si falla, reiniciar backend.

### Excel no guarda

Cerrar `PRESUPUESTO-TULUA2.xlsx` en Microsoft Excel y volver a intentar.

### Aparecen fórmulas como texto en el archivo

Abrir el archivo en Microsoft Excel y permitir recalculo. El sistema guarda fórmulas vivas, pero `openpyxl` no calcula resultados.

### Aparece `#N/D`

Revisar que el código del APU exista en `APU'S` y que el tipo de dato coincida con el modelo. La app conserva el tipo original del código cuando genera presupuesto.
