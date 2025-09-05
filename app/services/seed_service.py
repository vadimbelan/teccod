from __future__ import annotations

import logging
from typing import Iterable, List

from opensearchpy.helpers import bulk  # type: ignore

from app.models.schemas import DocumentIn, SeedResult
from app.opensearch.client import get_client
from app.opensearch.index import INDEX_NAME, create_index_if_not_exists

logger = logging.getLogger(__name__)


def _make_actions(docs: Iterable[DocumentIn]) -> List[dict]:
    actions: List[dict] = []
    for d in docs:
        actions.append(
            {
                "_op_type": "index",
                "_index": INDEX_NAME,
                "_source": {
                    "title": d.title,
                    "content": d.content,
                    "content_type": d.content_type,
                },
            }
        )
    return actions


def seed_demo_documents() -> SeedResult:
    create_index_if_not_exists()
    client = get_client()

    demo_docs: List[DocumentIn] = [
        DocumentIn(
            title="FastAPI basics",
            content="FastAPI is a modern web framework for building APIs with Python.",
            content_type="article",
        ),
        DocumentIn(
            title="Docker tips",
            content="Docker simplifies app deployment by packaging code with dependencies.",
            content_type="blog",
        ),
        DocumentIn(
            title="OpenSearch 2.13 release highlights",
            content="OpenSearch 2.13 brings improvements in performance and plugins.",
            content_type="news",
        ),
        DocumentIn(
            title="Weekly Infra Report",
            content="This report covers CI/CD, resource utilization, and incidents.",
            content_type="report",
        ),
        DocumentIn(
            title="Flask vs FastAPI",
            content="A quick comparison of Flask and FastAPI for microservices.",
            content_type="article",
        ),
    ]

    actions = _make_actions(demo_docs)
    logger.info("Seeding %d demo documents into index '%s' ...", len(actions), INDEX_NAME)
    success_count, errors = bulk(client, actions, raise_on_error=False)
    if errors:
        logger.warning("Bulk indexing completed with %d errors", len(errors))  # type: ignore[arg-type]
    return SeedResult(indexed=success_count, index=INDEX_NAME)
