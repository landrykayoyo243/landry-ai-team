from __future__ import annotations

from app.main import app


def test_health_status() -> None:
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    json_payload = response.json()
    assert json_payload["status"] == "ok"
    assert json_payload["healthy"] is True


def test_root_route() -> None:
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "initialized"
