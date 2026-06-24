from __future__ import annotations

try:
    from fastapi import FastAPI, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse
except ImportError:  # pragma: no cover
    FastAPI = None

# 1. Importaciones de Infraestructura Relacional
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Material  # Fuerza a SQLAlchemy a registrar el modelo

from app.api.crew import router as crew_router
from app.api.apus import router as apus_router
from app.api.budget import router as budget_router
from app.api.labor import router as labor_router
from app.api.materials import router as materials_router
from app.ui.apus_page import render_apus_page
from app.ui.materials_page import render_materials_page


def create_app():
    if FastAPI is None:
        raise RuntimeError(
            "FastAPI is not installed. Install backend requirements before running the API."
        )

    # 2. Inicialización automática del esquema (Enfoque SRE)
    # Revisa Postgres y crea las tablas que hagan falta en el arranque
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Gestor de Presupuestos APU", version="2.0.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 3. Health Check Avanzado para Monitoreo de Confiabilidad
    @app.get("/health", tags=["Infrastructure"])
    def health_check(db: Session = Depends(get_db)):
        try:
            # Prueba activa: intentamos consultar la tabla recién creada
            db.execute(Base.metadata.tables["materiales"].select().limit(1))
            return {
                "status": "healthy",
                "database": "connected",
                "version": "2.0.0"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }

    @app.get("/", response_class=HTMLResponse)
    def materials_app():
        return HTMLResponse(render_materials_page())

    @app.get("/apus", response_class=HTMLResponse)
    def apus_app():
        return HTMLResponse(render_apus_page())

    # Routers existentes se mantienen intactos
    app.include_router(materials_router, prefix="/api")
    app.include_router(labor_router, prefix="/api")
    app.include_router(crew_router, prefix="/api")
    app.include_router(apus_router, prefix="/api")
    app.include_router(budget_router, prefix="/api")

    return app


app = create_app() if FastAPI is not None else None