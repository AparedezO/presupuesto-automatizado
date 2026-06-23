from __future__ import annotations

from app.excel.labor_repository import LaborRepository
from app.schemas.labor import LaborCreate, LaborRead


class LaborService:
    def __init__(self, repository: LaborRepository | None = None) -> None:
        self.repository = repository or LaborRepository()

    def search(self, term: str) -> list[LaborRead]:
        return self.repository.search(term)

    def create(self, labor: LaborCreate) -> dict:
        return self.repository.add_equipment(labor)
