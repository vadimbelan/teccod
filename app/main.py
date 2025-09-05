from __future__ import annotations

import logging
from fastapi import FastAPI
from app.api.routes import router as api_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")


def create_app() -> FastAPI:
    app = FastAPI(
        title="OpenSearch FastAPI Demo",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(api_router)

    @app.get("/", tags=["root"])
    def root() -> dict[str, str]:
        return {"message": "OpenSearch FastAPI demo is running. See /docs"}

    return app


app = create_app()
