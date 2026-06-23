from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.paths import BACKUP_DIR, EXPORTS_DIR, WORKBOOK_PATH


@dataclass(frozen=True)
class Settings:
    workbook_path: Path = WORKBOOK_PATH
    backup_dir: Path = BACKUP_DIR
    exports_dir: Path = EXPORTS_DIR
    excel_engine: str = "openpyxl"


settings = Settings()
