from __future__ import annotations

import logging
from typing import Dict, Any, cast

from opensearchpy.exceptions import NotFoundError  # type: ignore

from app.core.config import settings
from app.opensearch.client import get_client

logger = logging.getLogger(__name__)

INDEX_NAME = settings.os_index_name

INDEX_BODY: Dict[str, Any] = {
    "settings": {
        "index": {"number_of_shards": 1, "number_of_replicas": 0},
        "analysis": {"analyzer": {"default": {"type": "standard"}}},
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "content_type": {"type": "keyword"},
        }
    },
}


def index_exists() -> bool:
    client = get_client()
    return bool(client.indices.exists(index=INDEX_NAME))


def create_index_if_not_exists() -> Dict[str, Any]:
    client = get_client()
    if index_exists():
        logger.info("Index '%s' already exists", INDEX_NAME)
        return {"acknowledged": True, "created": False, "index": INDEX_NAME}

    logger.info("Creating index '%s' ...", INDEX_NAME)
    resp = cast(Dict[str, Any], client.indices.create(index=INDEX_NAME, body=INDEX_BODY))
    return {"acknowledged": True, "created": True, "index": INDEX_NAME, "result": resp}


def get_cluster_health() -> Dict[str, Any]:
    client = get_client()
    try:
        return cast(Dict[str, Any], client.cluster.health())
    except NotFoundError:
        return {"status": "unknown"}
