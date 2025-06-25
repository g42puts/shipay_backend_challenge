from httpx import AsyncClient, ASGITransport

import pytest
from fastapi import FastAPI

from app.main import app, lifespan


@pytest.mark.asyncio
async def test_read_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_lifespan_prints_startup_message(capfd):
    app = FastAPI(title="Test App", description="Test Desc", docs_url="/docs")
    async with lifespan(app):
        pass
    out, _ = capfd.readouterr()
    assert "API Started" in out
    assert "Test App" in out
    assert "Test Desc" in out
    assert "/docs" in out
