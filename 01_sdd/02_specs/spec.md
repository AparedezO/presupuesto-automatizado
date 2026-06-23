# SPEC-001 - Gestor De Presupuestos APU

## 1. Visión General

Desarrollar una aplicación web local, responsive y orientada a escritorio/móvil para consultar, crear y organizar presupuestos eléctricos a partir del archivo Excel `PRESUPUESTO-TULUA2.xlsx`.

El libro Excel es la fuente de verdad. La aplicación no debe destruir fórmulas, formatos, rangos nombrados ni vínculos internos entre hojas.

## 2. Alcance Actual

Incluido:

- Consulta, búsqueda y creación de materiales.
- Sugerencia automática de códigos de materiales y APUs.
- Consulta y creación de APUs.
- Creación de APUs únicamente con materiales agregados manualmente desde la app.
- Inserción de filas estándar al final de cada APU: `E&H`, `GLV`, `T`, `H/C`.
- Inserción de una fila final en blanco al terminar cada APU, conservando fórmula en columna A.
- Construcción de presupuesto desde la app mediante selección de APUs y cantidad.
- Guardado del presupuesto en una nueva hoja basada en `PRESUPUESTO UNIFORCE`.
- Preservación de formatos, bordes, tipografías y fórmulas del modelo Excel.
- Interfaz con colores institucionales: rojo `rgb(192, 0, 0)`, gris `rgb(217, 217, 217)`, blanco y textos normales en negro.

Excluido por ahora:

- Edición de APUs existentes.
- Eliminación de materiales o APUs existentes.
- Recalculo nativo garantizado por Microsoft Excel desde la app.
- Multiusuario o ejecución en servidor remoto.

## 3. Stack Tecnológico

- Backend: FastAPI.
- Excel engine: `openpyxl`.
- Frontend: React + Vite + TypeScript.
- Estado frontend: Zustand.
- Validación backend: Pydantic.
- Pruebas backend: Pytest.

## 4. Modelo De Datos Excel

### 4.1 Libro Principal

Ruta:

```text
04_implementation/data/PRESUPUESTO-TULUA2.xlsx
```

Hojas principales:

- `L-MATERIALES`: catálogo de materiales.
- `APU'S`: análisis de precios unitarios.
- `PRESUPUESTO UNIFORCE`: plantilla base del presupuesto.
- `MANO DE OBRA`: referencias de mano de obra.
- `CUADRILLA`: referencias de cuadrillas.

### 4.2 Materiales - `L-MATERIALES`

Campos funcionales:

- `CODIGO`
- `DESCRIPCION`
- `MARCA`
- `UND`
- `FACTOR`
- `VALOR COSTO INCLUIDO IVA`
- `VALOR PRESUPUESTO`

Reglas:

- `CODIGO` debe ser único.
- Las columnas calculadas deben conservar fórmulas copiadas del modelo.
- Al guardar, se crea backup antes de reemplazar el archivo.

### 4.3 APUs - `APU'S`

Cada APU se compone de:

1. Fila cabecera con código, descripción, unidad y fórmulas de costo.
2. Fila de títulos.
3. Una o más filas de materiales agregados desde la app.
4. Filas estándar obligatorias: `E&H`, `GLV`, `T`, `H/C`.
5. Fila final en blanco.

Reglas:

- La app solo permite agregar materiales manuales al crear un nuevo APU.
- Las filas estándar siempre se agregan automáticamente.
- La fila final en blanco debe conservar fórmula en la columna A.
- Desde la fila inicial del APU hasta la fila final en blanco, la columna A debe repetir el código del APU mediante fórmula.
- Las fórmulas de `V/UNITARIO`, `V/PARCIAL`, costo total y mano de obra se deben inyectar como fórmulas vivas.
- El formato visual debe copiarse desde las filas modelo existentes del Excel.

### 4.4 Presupuesto - `PRESUPUESTO UNIFORCE`

La app permite construir una lista temporal de APUs y guardar un presupuesto nuevo.

Reglas de salida:

- La hoja nueva se crea copiando el formato de `PRESUPUESTO UNIFORCE`.
- Se conservan encabezados, celdas combinadas, estilos y formatos de las filas 1 a 5.
- Desde la fila 6 se escriben únicamente los APUs agregados desde la app.
- No deben quedar filas vacías intermedias entre el último APU y el bloque final.
- Inmediatamente después del último APU se copia el bloque predefinido equivalente a las filas 32 a 72 del modelo.
- La fórmula de subtotal de la columna J debe ajustarse a la cantidad real de APUs:

```excel
=SUM(J6:L{ultima_fila_apu})
```

Nota: Excel en español puede mostrar `SUMA`, pero internamente el archivo se escribe con función compatible en inglés.

- Las fórmulas de materiales y mano de obra del subtotal también deben apuntar al rango real de APUs.
- El código del APU debe escribirse con el mismo tipo de dato del modelo para evitar errores `#N/D` en búsquedas.

## 5. Requerimientos Funcionales

### MAT-001 - Buscar Materiales

El usuario puede buscar materiales por código o descripción.

Criterios de aceptación:

- La búsqueda filtra en tiempo real desde el frontend.
- Si no hay resultados, se muestra mensaje claro.
- El backend responde desde `GET /api/materials`.

Estado: implementado.

### MAT-002 - Crear Material

El usuario puede crear un material desde la app.

Criterios de aceptación:

- El sistema sugiere código a partir de la descripción.
- No permite códigos duplicados.
- Guarda en `L-MATERIALES`.
- Copia fórmulas y formatos de la fila modelo.
- Genera backup antes de guardar.

Estado: implementado.

### APU-001 - Buscar APUs

El usuario puede buscar APUs existentes por código o descripción.

Criterios de aceptación:

- La búsqueda consulta `GET /api/apus`.
- Si no hay resultados, se ofrece crear un nuevo APU.
- La vista es usable en escritorio y móvil.

Estado: implementado.

### APU-002 - Crear APU Con Materiales

El usuario puede crear un APU nuevo con datos de cabecera y materiales.

Criterios de aceptación:

- La app permite agregar materiales a una tabla temporal antes de guardar.
- Después de agregar un material, los campos quedan limpios para buscar/agregar otro.
- La cantidad usa controles `+` y `-`.
- Solo se permiten detalles de tipo material.
- Al guardar en Excel se mantienen formatos, bordes, tipografías y fórmulas del modelo.

Estado: implementado.

### APU-003 - Cierre Estandarizado De APU

Cada APU nuevo debe cerrar con filas estándar y fila final en blanco.

Criterios de aceptación:

- Al final de cada APU se agregan `E&H`, `GLV`, `T`, `H/C`.
- Después de `H/C` se agrega una fila en blanco.
- La columna A conserva fórmulas desde la cabecera hasta la fila en blanco.
- La columna A repite el código del APU dentro de todo el bloque creado.

Estado: implementado.

### APU-004 - Editar Como Nuevo Desde APU Similar

El usuario puede tomar un APU existente como base para crear otro APU nuevo.

Criterios de aceptación:

- En la lista de APUs existe un botón `Editar como nuevo` junto al botón `Agregar`.
- Al usarlo, la app carga la cabecera base y los materiales del APU seleccionado en el constructor.
- El APU original no se modifica.
- El constructor permite borrar materiales, agregar nuevos materiales y cambiar cantidades.
- Las filas estándar `E&H`, `GLV`, `T`, `H/C` no se cargan como materiales editables.
- Si una cantidad del APU base es fórmula de Excel, la app muestra su valor numérico cacheado y conserva la fórmula internamente para trasladarla al nuevo APU ajustando referencias de fila cuando se guarda sin cambiar.
- Al guardar, se crea un APU nuevo con el flujo normal de creación y preservación de fórmulas.

Estado: implementado.

### PRE-001 - Agregar APUs A Presupuesto En La App

El usuario puede agregar APUs a una lista de presupuesto dentro de la app.

Criterios de aceptación:

- Existe módulo `Presupuesto` en la navegación principal.
- Existe botón `+ Agregar APU` junto al flujo de APUs.
- El usuario puede elegir APU y cantidad.
- La lista temporal muestra los APUs seleccionados.

Estado: implementado.

### PRE-002 - Guardar Presupuesto En Excel

El usuario puede guardar el presupuesto en una hoja nueva.

Criterios de aceptación:

- Existe botón `Guardar presupuesto`.
- Se crea una hoja nueva con nombre seguro basado en `PRESUPUESTO`.
- La hoja usa el formato de `PRESUPUESTO UNIFORCE`.
- Solo aparecen las filas de APUs agregados.
- El bloque final del modelo aparece inmediatamente después de los APUs.
- Las fórmulas de subtotal se ajustan al número real de APUs.
- Se evita `#N/D` por diferencias entre código numérico y texto cuando el APU existe en el modelo.

Estado: implementado.

### PRE-003 - Exportar Archivo Filtrado Por Presupuesto

El usuario puede generar un archivo Excel nuevo para seguimiento, basado en el modelo completo pero reducido al alcance del presupuesto armado en la app.

Criterios de aceptación:

- La pantalla de presupuesto permite escribir un código de archivo para nombrar la exportación.
- El archivo nuevo se guarda en `06_delivery/exports`.
- El archivo conserva todas las hojas del modelo.
- La hoja `PRESUPUESTO` contiene el presupuesto generado desde la app.
- La hoja `APU'S` queda filtrada para conservar solo los APUs usados en la hoja de presupuesto.
- La hoja `L-MATERIALES` queda filtrada para conservar solo los materiales usados por esos APUs.
- El archivo fuente `PRESUPUESTO-TULUA2.xlsx` no se modifica durante esta exportación.
- Si un APU aparece varias veces en el presupuesto, se escribe una sola vez en la hoja `APU'S` filtrada.

Estado: implementado.

### UI-001 - Identidad Visual Institucional

La interfaz debe usar colores institucionales.

Criterios de aceptación:

- Rojo principal: `rgb(192, 0, 0)`.
- Gris: `rgb(217, 217, 217)`.
- Blanco para fondos/tarjetas.
- Textos normales en negro.
- Encabezados y botones pueden usar rojo.

Estado: implementado.

## 6. Requerimientos No Funcionales

### NFR-001 - Preservación Estricta De Fórmulas

El sistema debe proteger fórmulas existentes.

Criterios de aceptación:

- Antes de guardar se toma snapshot de fórmulas.
- Después de modificar se compara contra el snapshot.
- Si una fórmula existente cambia o desaparece, se bloquea el guardado.
- Solo se permiten fórmulas nuevas en filas/hojas generadas por la operación.

Estado: implementado.

### NFR-002 - Backups

Cada guardado exitoso debe crear una copia de seguridad.

Criterios de aceptación:

- El backup se crea antes de reemplazar el archivo principal.
- Los backups se guardan en `04_implementation/data/backups`.

Estado: implementado.

### NFR-003 - Ejecución Local

La aplicación se ejecuta localmente en Windows con PowerShell.

Criterios de aceptación:

- Backend disponible en `http://127.0.0.1:8000`.
- Frontend disponible en `http://127.0.0.1:5173`.
- CORS permite el consumo local entre frontend y backend.

Estado: implementado.

## 7. API Funcional

Endpoints principales:

- `GET /health`
- `GET /api/materials`
- `GET /api/materials/suggest-code`
- `POST /api/materials`
- `GET /api/apus`
- `GET /api/apus/suggest-code`
- `GET /api/apus/{row_number}/draft`
- `POST /api/apus`
- `GET /api/labor`
- `POST /api/labor`
- `GET /api/crew`
- `GET /api/budget`
- `POST /api/budget/apus`
- `POST /api/budget/save`
- `POST /api/budget/export`

## 8. Validación Automatizada

Pruebas actuales:

- Lectura de materiales y APUs desde Excel.
- Creación de material preservando fórmulas.
- Sugerencia de código único.
- Creación de APU con fórmulas, filas estándar y fila final en blanco.
- Carga de APU existente como borrador editable sin incluir filas estándar.
- Agregado de APU a presupuesto.
- Guardado de presupuesto con formato del modelo y bloque final dinámico.
- Exportación de archivo nuevo con presupuesto, APUs y materiales filtrados.
- Endpoints API principales.

Comando:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m pytest -q
```

Resultado esperado actual:

```text
10 passed
```

## 9. Próximos Cambios Recomendados

- Agregar previsualización de la hoja presupuesto antes de guardar.
- Permitir configurar el nombre de hoja desde la UI con validación visual.
- Agregar pruebas visuales/manuales documentadas para Excel abierto en Microsoft Excel.
- Evaluar `xlwings` si se requiere recalculo nativo inmediato de fórmulas.
- Agregar empaquetado o script único de arranque para usuario final.
