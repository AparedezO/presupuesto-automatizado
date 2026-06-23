from __future__ import annotations

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.schemas.crew import CrewRead
from app.excel.crew_repository import CrewRepository


router = APIRouter(prefix="/crew", tags=["crew"])


class CrewSearchResponse(BaseModel):
    items: list[CrewRead]
    total: int
    search: str
    can_create: bool = False


def get_repository() -> CrewRepository:
    return CrewRepository()


@router.get("", response_model=CrewSearchResponse)
def search_crew(
    search: str = Query(default=""),
    limit: int = Query(default=80, ge=1, le=500),
):
    repository = get_repository()
    items = repository.search(search)
    return CrewSearchResponse(
        items=items[:limit],
        total=len(items),
        search=search.strip(),
        can_create=False,
    )
