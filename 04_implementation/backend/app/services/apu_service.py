from __future__ import annotations

from app.excel.apu_repository import ApuRepository
from app.schemas.apus import ApuCreate, ApuDraftRead, ApuRead
from app.services.code_generator import generate_material_code


class ApuService:
    def __init__(self, repository: ApuRepository | None = None) -> None:
        self.repository = repository or ApuRepository()

    def suggest_code(self, description: str) -> str:
        return generate_material_code(description, max_length=28)

    def search(self, term: str) -> list[ApuRead]:
        return self.repository.search(term)

    def create(self, apu: ApuCreate) -> dict:
        return self.repository.create_apu(apu)

    def draft_from_row(self, row_number: int) -> ApuDraftRead:
        return self.repository.get_draft_from_row(row_number)
