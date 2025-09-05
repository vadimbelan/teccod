from __future__ import annotations

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional

from app.core.config import settings


AllowedContentType = Literal["article", "blog", "news", "report"]


class DocumentIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=512)
    content: str = Field(..., min_length=1)
    content_type: AllowedContentType

    @validator("content_type")
    def validate_content_type(cls, v: str) -> str:  # noqa: N805
        allowed = set(settings.content_types)
        if v not in allowed:
            raise ValueError(f"content_type must be one of {sorted(allowed)}")
        return v


class DocumentOut(BaseModel):
    id: str
    title: str
    content_type: AllowedContentType


class SeedResult(BaseModel):
    indexed: int
    index: str
