from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.core.config import settings
from app.opensearch.client import get_client
from app.opensearch.index import INDEX_NAME

logger = logging.getLogger(__name__)

SNIPPET_LEN = 50


def _make_snippet(text: str, max_len: int = SNIPPET_LEN) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len]


def search_documents(
    q: str, content_type: Optional[str] = None, size: int = 10
) -> List[Dict[str, str]]:
    if not q or not q.strip():
        raise HTTPException(
            status_code=422, detail="Query parameter 'q' must be non-empty"
        )

    if content_type is not None:
        allowed = set(settings.content_types)
        if content_type not in allowed:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid content_type. Allowed: {sorted(allowed)}",
            )

    client = get_client()

    query: Dict[str, Any] = {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": q,
                        "fields": ["title^2", "content"],
                        "operator": "and",
                    }
                }
            ],
            "filter": [],
        }
    }

    if content_type:
        query["bool"]["filter"].append({"term": {"content_type": content_type}})

    logger.info("Search query: %s", query)

    resp = client.search(
        index=INDEX_NAME,
        body={"query": query, "_source": ["title", "content"], "size": size},
    )

    hits = resp.get("hits", {}).get("hits", [])
    results: List[Dict[str, str]] = []
    for h in hits:
        src = h.get("_source", {}) or {}
        title = str(src.get("title", ""))
        content = str(src.get("content", ""))
        results.append(
            {
                "title": title,
                "snippet": _make_snippet(content, SNIPPET_LEN),
            }
        )

    return results
