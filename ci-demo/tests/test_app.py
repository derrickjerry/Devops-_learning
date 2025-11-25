import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_todos(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_todo_success(client):
    response = client.post("/todos", json={"task": "Write tests"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["task"] == "Write tests"


def test_add_todo_invalid(client):
    response = client.post("/todos", json={})
    assert response.status_code == 400


def test_delete_todo(client):
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert "deleted" in response.get_json()["message"]
