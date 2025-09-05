from __future__ import annotations

from typing import Optional, List, Dict

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.opensearch.index import create_index_if_not_exists, index_exists, get_cluster_health
from app.services.seed_service import seed_demo_documents
from app.models.schemas import SeedResult
from app.services.search_service import search_documents
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


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


@router.get("/search", tags=["search"])
def search(
    q: str = Query(..., min_length=1, description="Ключевое слово для поиска"),
    content_type: Optional[str] = Query(None, description="Фильтр по типу контента (term)"),
    size: int = Query(10, ge=1, le=100, description="Максимум документов в ответе"),
) -> List[Dict[str, str]]:
    try:
        return search_documents(q=q, content_type=content_type, size=size)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Search error: {exc}") from exc


@router.get("/ui", response_class=HTMLResponse, tags=["ui"])
def ui(
    request: Request,
    q: Optional[str] = Query(None),
    content_type: Optional[str] = Query(None),
) -> HTMLResponse:
    results: List[Dict[str, str]] = []
    error: Optional[str] = None

    if q:
        ct = None if (content_type in (None, "", "any")) else content_type
        try:
            results = search_documents(q=q, content_type=ct, size=20)
        except HTTPException as exc:  # ошибки валидации/422
            error = str(exc.detail)
        except Exception as exc:  # noqa: BLE001
            error = f"Search error: {exc}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "q": q or "",
            "content_type": content_type or "any",
            "content_types": ["any", *settings.content_types],
            "results": results,
            "error": error,
        },
    )
