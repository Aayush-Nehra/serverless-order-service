import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.repo.create_order")
def test_create_order(mock_create_order):
    order_data = {"user_id": "user1", "amount": 123.45}
    mock_create_order.return_value = {
        "order_id": "test-id",
        "user_id": "user1",
        "amount": 123.45,
        "status": "CREATED",
        "created_at": "2025-12-23T00:00:00",
    }

    response = client.post("/orders", json=order_data)

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user1"
    assert data["amount"] == 123.45
    assert data["status"] == "CREATED"
    assert data["order_id"] == "test-id"
    assert data["created_at"] == "2025-12-23T00:00:00"


@patch("app.main.repo.get_order")
def test_get_order_success(mock_get_order):
    mock_get_order.return_value = {
        "order_id": "test-id",
        "user_id": "user1",
        "amount": 123.45,
        "status": "CREATED",
        "created_at": "2025-12-23T00:00:00",
    }

    response = client.get("/orders/test-id")

    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == "test-id"
    assert data["user_id"] == "user1"
    assert data["amount"] == 123.45
    assert data["status"] == "CREATED"
    assert data["created_at"] == "2025-12-23T00:00:00"
