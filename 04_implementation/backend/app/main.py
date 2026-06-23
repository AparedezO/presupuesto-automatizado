from __future__ import annotations

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse
except ImportError:  # pragma: no cover - local dependencies may not be installed yet.
    FastAPI = None

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

    app = FastAPI(title="Gestor de Presupuestos APU", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    def materials_app():
        return HTMLResponse(render_materials_page())

    @app.get("/apus", response_class=HTMLResponse)
    def apus_app():
        return HTMLResponse(render_apus_page())

    app.include_router(materials_router, prefix="/api")
    app.include_router(labor_router, prefix="/api")
    app.include_router(crew_router, prefix="/api")
    app.include_router(apus_router, prefix="/api")
    app.include_router(budget_router, prefix="/api")

    return app


app = create_app() if FastAPI is not None else None
