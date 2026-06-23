from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


def create_workbook_backup(workbook_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{workbook_path.stem}_{timestamp}{workbook_path.suffix}"
    shutil.copy2(workbook_path, backup_path)
    return backup_path
