# ADR-001 - Motor De Escritura Excel

## Estado

Aceptada.

## Contexto

El archivo `PRESUPUESTO-TULUA2.xlsx` contiene fórmulas nativas, formatos, celdas combinadas, rangos definidos y vínculos entre hojas. La aplicación debe modificarlo sin convertirlo en datos planos y sin perder fórmulas.

Los flujos actuales escriben en:

- `L-MATERIALES` para materiales nuevos.
- `APU'S` para APUs nuevos.
- Hojas nuevas de presupuesto basadas en `PRESUPUESTO UNIFORCE`.

## Decisión

Usar `openpyxl` como motor inicial de lectura y escritura, encapsulado detrás de `ExcelWorkbook` y repositorios especializados.

La lógica de escritura no se reparte en la API ni en el frontend. Toda operación sobre Excel debe pasar por la capa `app/excel`.

## Reglas Aceptadas

- Crear backup antes de guardar.
- Tomar snapshot de fórmulas antes de modificar.
- Comparar fórmulas después de modificar.
- Bloquear guardado si una fórmula existente cambia o desaparece.
- Registrar fórmulas nuevas permitidas cuando se insertan filas o bloques nuevos.
- Copiar estilos, bordes, formatos, alineaciones y alturas desde filas/hojas modelo.
- Escribir fórmulas vivas, no valores estáticos, en columnas calculadas.
- Marcar el libro para recálculo automático al guardar.

## Reglas Específicas De APU

- Los APUs nuevos se construyen copiando filas modelo de `APU'S`.
- Solo se permite agregar materiales desde la app.
- Siempre se agregan filas estándar `E&H`, `GLV`, `T`, `H/C`.
- Siempre se agrega una fila final en blanco.
- La columna A debe mantener fórmula desde la cabecera hasta la fila final en blanco para repetir el código del APU.

## Reglas Específicas De Presupuesto

- Cada guardado crea una hoja nueva basada en `PRESUPUESTO UNIFORCE`.
- Se preservan encabezados de filas 1 a 5.
- Solo se escriben las filas de APUs agregados desde la app.
- El bloque final equivalente a filas 32 a 72 del modelo se copia inmediatamente después del último APU.
- Las fórmulas de subtotal deben adaptarse al número real de APUs.
- El código del APU debe conservar su tipo original para evitar errores de búsqueda `#N/D`.

## Alternativas Consideradas

### `xlwings`

Ventajas:

- Recalculo nativo con Microsoft Excel.
- Mayor compatibilidad visual con objetos complejos.

Desventajas:

- Requiere Excel instalado.
- Depende de automatización COM en Windows.
- Más difícil de ejecutar en entornos automatizados o pruebas headless.

### Escritura plana con CSV/JSON

Descartada porque destruiría fórmulas, estilos y vínculos del modelo Excel.

## Consecuencias

- La implementación actual es suficiente para preservar fórmulas y formatos en los flujos definidos.
- Si se requiere recalculo inmediato o compatibilidad total con elementos visuales avanzados, se evaluará migrar internamente a `xlwings` manteniendo la interfaz de repositorios.
- Si el usuario modifica filas modelo en Excel, hay que revisar las constantes de plantilla usadas por los repositorios.
