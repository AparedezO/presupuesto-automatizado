# TASK-001 - Materiales, APUs Y Presupuesto Base

## Especificación Relacionada

`SPEC-001 - Gestor De Presupuestos APU`

## Objetivo

Implementar la primera versión funcional local para consultar y crear materiales, crear APUs con materiales y generar presupuestos en una hoja nueva basada en el modelo Excel.

## Entregables

- Backend FastAPI con endpoints de materiales, APUs, mano de obra, cuadrillas y presupuesto.
- Frontend React/Vite con navegación: Materiales, APUs y Presupuesto.
- Escritura segura sobre `PRESUPUESTO-TULUA2.xlsx`.
- Pruebas automatizadas de integridad Excel.
- Documentación SDD actualizada.

## Pasos

1. Crear capa Excel con backups y verificación de fórmulas.
2. Implementar lectura y creación de materiales.
3. Implementar búsqueda y creación de APUs.
4. Agregar cierre estándar de APU con `E&H`, `GLV`, `T`, `H/C` y fila final en blanco.
5. Implementar lista temporal de presupuesto en frontend.
6. Implementar guardado de presupuesto en hoja nueva con formato `PRESUPUESTO UNIFORCE`.
7. Ajustar subtotales dinámicos según cantidad de APUs.
8. Agregar flujo `Editar como nuevo` para crear APUs desde una base similar.
9. Aplicar identidad visual institucional.
10. Validar con pruebas backend y build frontend.

## Criterios De Finalización

- `pytest -q` pasa en backend.
- `npm run build` pasa en frontend.
- Crear material no modifica fórmulas existentes.
- Crear APU agrega materiales, filas estándar y fila final en blanco.
- Editar como nuevo carga materiales del APU base sin incluir filas estándar.
- Guardar presupuesto crea hoja nueva sin filas vacías intermedias antes del bloque final.
- Fórmulas de subtotal apuntan al rango real de APUs.

## Estado

Implementado.

## Evidencia

- Pruebas backend: `10 passed`.
- Build frontend: exitoso con Vite.
- Endpoints locales verificados:
  - `GET http://127.0.0.1:8000/health`
  - `GET http://127.0.0.1:8000/api/materials`
  - `GET http://127.0.0.1:8000/api/apus`
