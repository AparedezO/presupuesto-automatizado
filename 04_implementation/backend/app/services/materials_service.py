from __future__ import annotations

from app.excel.materials_repository import MaterialsRepository
from app.schemas.materials import MaterialCreate, MaterialRead
from app.services.code_generator import generate_material_code


class MaterialsService:
    def __init__(self, repository: MaterialsRepository | None = None) -> None:
        self.repository = repository or MaterialsRepository()

    def suggest_code(self, description: str) -> str:
        base_code = generate_material_code(description)
        if not self.repository.exists(base_code):
            return base_code

        suffix = 2
        while self.repository.exists(f"{base_code}-{suffix}"):
            suffix += 1
        return f"{base_code}-{suffix}"

    def search(self, term: str) -> list[MaterialRead]:
        return self.repository.search(term)

    def create(self, material: MaterialCreate) -> dict:
        return self.repository.add_material(material)
