# Presupuesto Automatizado 2.0

Aplicación local de alta velocidad para gestionar materiales, APUs y presupuestos eléctricos. Diseñada bajo una arquitectura relacional con sincronización diferida hacia el libro maestro `PRESUPUESTO-TULUA2.xlsx`.

## 🚀 Estado y Características

Versión funcional alineada con `SPEC-001` en proceso de migración arquitectónica hacia un motor relacional sólido:

- **Gestión Eficiente:** Búsqueda y creación instantánea de materiales y APUs en milisegundos.
- **Generación de APUs:** Estructuración automática con materiales, filas estándar y fila final limpia.
- **Módulo de Presupuesto:** Consolidación y guardado dinámico en hojas nuevas.
- **Preservación Integral (`NFR-001`):** Respeto absoluto de fórmulas nativas, formatos geométricos y generación automática de backups.
- **Interfaz de Usuario:** Frontend responsive optimizado con la paleta de colores institucionales.

---

## 🏗️ Evolución de Arquitectura: Motor Relacional y Sincronización

Para garantizar la escalabilidad, la velocidad de respuesta y la inmunidad contra la corrupción de datos, el sistema implementa un flujo desacoplado:

- **Motor Transaccional (PostgreSQL):** Actúa como el núcleo de trabajo en caliente. Todas las consultas, ediciones y altas corren en la base de datos, liberando al archivo Excel de operaciones I/O concurrentes y pesadas.
- **Aislamiento del Maestro:** El archivo Excel central opera estrictamente como plantilla base y motor final de consolidación o firmas.
- **Flujo de Trabajo Diferido:** Los nuevos registros se marcan localmente con el estado `pendientes_sync`. El botón **Sincronizar Maestro** vuelca los cambios en lote de forma segura y controlada.
- **Exportación Segura:** El sistema bloquea de manera inteligente la generación del archivo "Filtrado" si detecta que existen cambios en la base de datos que aún no han sido sincronizados en el Excel maestro.

---

## 📁 Estructura SDD (Spec-Driven Development)

El proyecto sigue una jerarquía rigurosa de documentación técnica y trazabilidad:

- `PROJECT_CONTEXT.md`: Contexto ejecutivo y objetivos generales del proyecto.
- `01_sdd/02_specs/spec.md`: Especificación funcional y de requerimientos principal.
- `01_sdd/05_traceability/TRACEABILITY_MATRIX.md`: Matriz de trazabilidad (Requisito - Código - Prueba).
- `02_design/architecture/ARCHITECTURE.md`: Documentación formal de la arquitectura técnica.
- `02_design/decisions/ADR-001-excel-write-engine.md`: Registro de decisiones de diseño (Motor de manipulación Excel).
- `03_planning/tasks/TASK-001-modulos-materiales-apus-presupuesto.md`: Control y desglose de tareas implementadas.
- `05_validation/test_plans/VALIDATION_PLAN.md`: Plan maestro y estrategia de validación.
- `05_validation/evidence/VALIDATION_REPORT.md`: Registro de evidencias de aceptación de pruebas.
- `06_delivery/RUNBOOK.md`: Guía técnica de despliegue, mantenimiento y entrega local.

---

## 🛠️ Ejecución en Entorno Local (VS Code)

### 1. Levantar la Base de Datos (PostgreSQL)

Asegúrate de tener Docker Desktop ejecutándose en segundo plano. En la raíz del proyecto, abre una terminal y corre:

```powershell
docker compose up -d
2. Levantar el Backend (FastAPI)
PowerShell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
3. Levantar el Frontend (React + Vite)
PowerShell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run dev -- --host 127.0.0.1 --port 5173
URL de acceso en el navegador: http://127.0.0.1:5173

🧪 Pruebas y Validación
Pruebas unitarias del Backend (Pytest):

PowerShell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\backend"
.\.venv\Scripts\python.exe -m pytest -q
Validación de empaquetado del Frontend:

PowerShell
cd "D:\PROGRAMACION\04_Presupuesto Automatizado 2.0\04_implementation\frontend"
npm run build
⚠️ Notas Operativas Importantes
Bloqueo de Archivos de Windows: Mantén completamente cerrado el archivo maestro 04_implementation/data/PRESUPUESTO-TULUA2.xlsx mientras ejecutas la aplicación o realizas la sincronización en bloque. Si Excel mantiene el archivo abierto en memoria, el sistema operativo denegará los permisos de escritura a openpyxl, interrumpiendo el flujo de datos.
```
