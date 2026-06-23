# Configuración Git Del Proyecto

## Objetivo

Versionar código y documentación sin subir información privada, archivos fuente del cliente ni artefactos generados.

## Archivos Que Sí Deben Versionarse

- Documentación SDD: `01_sdd`, `02_design`, `03_planning`, `05_validation`, `06_delivery`.
- Código backend: `04_implementation/backend/app`.
- Pruebas backend: `04_implementation/backend/tests`.
- Código frontend: `04_implementation/frontend/src`.
- Archivos de dependencias:
  - `04_implementation/backend/requirements.txt`
  - `04_implementation/frontend/package.json`
  - `04_implementation/frontend/package-lock.json`

## Archivos Privados O Generados Que No Deben Versionarse

- Libro fuente Excel:
  - `04_implementation/data/PRESUPUESTO-TULUA2.xlsx`
- Backups del Excel:
  - `04_implementation/data/backups/`
- Entornos locales:
  - `04_implementation/backend/.venv/`
  - `node_modules/`
- Build frontend:
  - `04_implementation/frontend/dist/`
- Cache local:
  - `04_implementation/frontend/.npm-cache/`
  - `.pytest_cache/`
  - `__pycache__/`
- Variables de entorno y secretos:
  - `.env`
  - `.env.*`
  - llaves `*.key`, `*.pem`, `*.p12`, `*.pfx`
- Entregables generados o evidencias con datos privados:
  - `06_delivery/exports/`
  - archivos Excel/PDF/imagen dentro de `05_validation/evidence/`
- Archivos temporales de Excel:
  - `~$*.xlsx`

## Inicialización

Desde la raíz:

```powershell
git init -b main
git status
```

## Antes Del Primer Commit

Revisar:

```powershell
git status --short
git check-ignore -v "04_implementation/data/PRESUPUESTO-TULUA2.xlsx"
git check-ignore -v "04_implementation/backend/.venv"
git check-ignore -v "04_implementation/frontend/node_modules"
```

Si todo está correcto:

```powershell
git add .
git status --short
git commit -m "Initial project documentation and app baseline"
```

## Nota Importante

El archivo Excel privado debe copiarse manualmente en `04_implementation/data/` en cada equipo donde se ejecute la app. No debe subirse al repositorio remoto.
