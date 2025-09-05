from __future__ import annotations

import os
import pytest
import requests

API = os.getenv("TEST_API_URL", "http://localhost:8000")


@pytest.mark.integration
def test_search_fastapi():
    r = requests.get(f"{API}/search", params={"q": "FastAPI"})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any("FastAPI" in (item.get("title") or "") for item in data)


@pytest.mark.integration
def test_search_filter_content_type():
    r = requests.get(f"{API}/search", params={"q": "Docker", "content_type": "blog"})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any("Docker tips" in (item.get("title") or "") for item in data)
