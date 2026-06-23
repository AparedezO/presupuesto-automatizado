from __future__ import annotations

from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = Path(__file__).resolve().parents[2]
IMPLEMENTATION_DIR = Path(__file__).resolve().parents[3]
PROJECT_DIR = IMPLEMENTATION_DIR.parent

DATA_DIR = IMPLEMENTATION_DIR / "data"
BACKUP_DIR = DATA_DIR / "backups"
WORKBOOK_PATH = DATA_DIR / "PRESUPUESTO-TULUA2.xlsx"
EXPORTS_DIR = PROJECT_DIR / "06_delivery" / "exports"
