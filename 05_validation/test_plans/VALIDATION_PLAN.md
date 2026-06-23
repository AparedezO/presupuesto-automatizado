# Plan De Validación

## Objetivo

Confirmar que la aplicación cumple `SPEC-001` sin romper el libro Excel base.

## Alcance

Validar:

- Consulta de materiales.
- Creación de materiales.
- Consulta de APUs.
- Creación de APUs.
- Cierre estándar de APUs con fila final en blanco.
- Armado y guardado de presupuesto.
- Preservación de fórmulas y formatos.
- Ejecución local backend/frontend.

## Validación Automatizada

### Backend

Comando:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m pytest -q
```

Criterio de aprobación:

- Todas las pruebas deben pasar.
- No deben existir errores de integridad de fórmulas.

### Frontend

Comando:

```powershell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run build
```

Criterio de aprobación:

- El build debe finalizar sin errores.

## Validación Manual

### Materiales

1. Abrir `http://127.0.0.1:5173`.
2. Entrar a `Materiales`.
3. Buscar un material existente.
4. Buscar un material inexistente.
5. Crear un material nuevo.
6. Confirmar en Excel que se agregó fila y se conservaron fórmulas.

### APUs

1. Entrar a `APUs`.
2. Buscar un APU existente.
3. Crear APU nuevo.
4. Agregar uno o más materiales.
5. Confirmar que cada material agregado aparece en tabla temporal.
6. Guardar APU.
7. Confirmar en Excel:
   - Cabecera.
   - Filas de materiales.
   - Filas `E&H`, `GLV`, `T`, `H/C`.
   - Fila final en blanco.
   - Fórmula en columna A hasta la fila final en blanco.

### APUs - Editar Como Nuevo

1. Entrar a `APUs`.
2. Buscar un APU similar al que se quiere crear.
3. Hacer clic en `Editar como nuevo`.
4. Confirmar que el constructor carga materiales y cantidades del APU base.
5. Borrar un material.
6. Agregar un material nuevo.
7. Cambiar cantidades con `+` y `-`.
8. Cambiar descripcion y codigo.
9. Guardar.
10. Confirmar en Excel que se creo un APU nuevo y el APU base no cambio.

### Presupuesto

1. Entrar a `Presupuesto`.
2. Agregar uno o más APUs con cantidad.
3. Guardar presupuesto.
4. Confirmar en Excel:
   - Hoja nueva creada.
   - Encabezado igual a `PRESUPUESTO UNIFORCE`.
   - Solo aparecen los APUs agregados.
   - El bloque final aparece inmediatamente después del último APU.
   - La fórmula de subtotal en columna J apunta al rango real.

### Presupuesto - Exportar Archivo Filtrado

1. Entrar a `Presupuesto`.
2. Agregar uno o más APUs con cantidad.
3. Escribir un código de archivo, por ejemplo `TULUA-001`.
4. Hacer clic en `Generar archivo filtrado`.
5. Confirmar que se crea un archivo `.xlsx` en `06_delivery/exports`.
6. Abrir el archivo generado y confirmar:
   - Conserva las hojas del modelo.
   - La hoja `PRESUPUESTO` contiene solo los APUs del presupuesto armado.
   - La hoja `APU'S` contiene solo los APUs usados por el presupuesto.
   - La hoja `L-MATERIALES` contiene solo materiales usados por esos APUs.
   - El archivo fuente original no se modifica.

## Criterios De No Regresión

- No se eliminan fórmulas existentes.
- No se cambian fórmulas existentes fuera de los bloques creados.
- No se pierden bordes, fuentes ni celdas combinadas del presupuesto.
- No se guardan códigos APU con tipo incorrecto que genere `#N/D`.
- La app sigue funcionando con backend en `8000` y frontend en `5173`.
