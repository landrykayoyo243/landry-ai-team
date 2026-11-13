from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import Agent
from app.database.session import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    with TestingSession() as db:
        db.add_all([
            Agent(name="LANDRY MANAGER", role="manager", description="Project manager"),
            Agent(name="LANDRY CODER", role="coder", description="Developer"),
            Agent(name="LANDRY REVIEWER", role="reviewer", description="Auditor"),
        ])
        db.commit()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


def register_and_login(client: TestClient, email: str = "owner@example.com") -> str:
    response = client.post("/api/v1/auth/register", json={"email": email, "full_name": "Test Owner", "password": "strong-password-123"})
    assert response.status_code == 201
    response = client.post("/api/v1/auth/login", data={"username": email, "password": "strong-password-123"})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_authentication_and_private_route(client: TestClient):
    assert client.get("/api/v1/projects").status_code == 401
    token = register_and_login(client)
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 200


def test_project_crud_and_forbidden_access(client: TestClient):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    project = client.post("/api/v1/projects", headers=headers, json={"name": "Demo"})
    assert project.status_code == 201
    assert client.get(f"/api/v1/projects/{project.json()['id']}", headers=headers).status_code == 200

    other_token = register_and_login(client, "other@example.com")
    denied = client.get(f"/api/v1/projects/{project.json()['id']}", headers={"Authorization": f"Bearer {other_token}"})
    assert denied.status_code == 403


def test_conversation_message_task_and_review(client: TestClient):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    project = client.post("/api/v1/projects", headers=headers, json={"name": "Backend"}).json()
    agents = client.get("/api/v1/agents", headers=headers).json()
    manager_id = next(agent["id"] for agent in agents if agent["role"] == "manager")
    coder_id = next(agent["id"] for agent in agents if agent["role"] == "coder")
    conversation = client.post("/api/v1/conversations", headers=headers, json={"title": "Planning", "agent_id": manager_id, "project_id": project["id"]})
    assert conversation.status_code == 201
    message = client.post(f"/api/v1/conversations/{conversation.json()['id']}/messages", headers=headers, json={"content": "Build the API"})
    assert message.status_code == 201
    assert client.get(f"/api/v1/conversations/{conversation.json()['id']}/messages", headers=headers).json()[0]["content"] == "Build the API"
    task = client.post(f"/api/v1/projects/{project['id']}/tasks", headers=headers, json={"title": "Implement models", "assignee_id": coder_id})
    assert task.status_code == 201
    assert task.json()["assignee_id"] == coder_id
    assert client.patch(f"/api/v1/tasks/{task.json()['id']}", headers=headers, json={"status": "completed"}).json()["status"] == "completed"
    review = client.post(f"/api/v1/projects/{project['id']}/reviews", headers=headers, json={"verdict": "APPROVED", "findings": "All checks passed", "task_id": task.json()["id"]})
    assert review.status_code == 201
    assert client.get(f"/api/v1/projects/{project['id']}/progress", headers=headers).json()["completion_percent"] == 100


def test_password_is_hashed_and_invalid_input_rejected(client: TestClient):
    register_and_login(client)
    assert client.post("/api/v1/auth/register", json={"email": "bad@example.com", "full_name": "Bad", "password": "short"}).status_code == 422
