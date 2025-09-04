from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv


load_dotenv()

DEFAULT_CONTENT_TYPES = ["article", "blog", "news", "report"]


@dataclass(frozen=True)
class Settings:
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    os_host: str = os.getenv("OS_HOST", "opensearch")
    os_port: int = int(os.getenv("OS_PORT", "9200"))
    os_user: str | None = os.getenv("OS_USER")
    os_password: str | None = os.getenv("OS_PASSWORD")
    os_use_ssl: bool = os.getenv("OS_USE_SSL", "false").lower() == "true"
    os_verify_certs: bool = os.getenv("OS_VERIFY_CERTS", "false").lower() == "true"
    os_index_name: str = os.getenv("OS_INDEX_NAME", "documents")

    content_types_env: str = os.getenv("CONTENT_TYPES", "article,blog,news,report")

    @property
    def content_types(self) -> List[str]:
        parts = [p.strip() for p in self.content_types_env.split(",") if p.strip()]
        return parts if parts else DEFAULT_CONTENT_TYPES


settings = Settings()
