from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.opensearch.index import create_index_if_not_exists, index_exists, get_cluster_health
from app.services.seed_service import seed_demo_documents
from app.models.schemas import SeedResult

router = APIRouter()


@router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/os_health", tags=["system"])
def os_health() -> dict:
    try:
        return get_cluster_health()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"OpenSearch health error: {exc}") from exc


@router.post("/init_index", tags=["index"])
def init_index() -> dict:
    try:
        result = create_index_if_not_exists()
        return {
            "index_exists": index_exists(),
            "details": result,
        }
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Init index error: {exc}") from exc


@router.post("/seed", response_model=SeedResult, tags=["data"])
def seed() -> SeedResult:
    try:
        return seed_demo_documents()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Seed error: {exc}") from exc
