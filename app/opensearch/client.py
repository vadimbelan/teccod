from __future__ import annotations

import logging
from typing import Optional, List, Dict, Any

from opensearchpy import OpenSearch  # type: ignore

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[OpenSearch] = None


def get_client() -> OpenSearch:
    global _client
    if _client is not None:
        return _client

    scheme = "https" if settings.os_use_ssl else "http"

    hosts: List[Dict[str, Any]] = [
        {
            "host": settings.os_host,
            "port": settings.os_port,
            "scheme": scheme,
        }
    ]

    http_auth = None
    if settings.os_user and settings.os_password:
        http_auth = (settings.os_user, settings.os_password)

    logger.info(
        "Initializing OpenSearch client: host=%s port=%s scheme=%s verify_certs=%s",
        settings.os_host,
        settings.os_port,
        scheme,
        settings.os_verify_certs,
    )

    _client = OpenSearch(
        hosts=hosts,
        http_auth=http_auth,
        use_ssl=settings.os_use_ssl,
        verify_certs=settings.os_verify_certs,
        ssl_show_warn=False,
        timeout=10,
        max_retries=3,
        retry_on_timeout=True,
    )
    return _client
