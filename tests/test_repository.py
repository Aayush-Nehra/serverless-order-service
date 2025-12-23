import pytest
from unittest.mock import patch, MagicMock
from app.repository import OrderRepository, OrderCreate
import botocore


@patch("app.repository.table")
def test_create_order_success(mock_table):
    repo = OrderRepository()
    order = OrderCreate(user_id="user1", amount=100.0)
    mock_table.put_item.return_value = None
    result = repo.create_order(order)
    assert result["user_id"] == "user1"
    assert float(result["amount"]) == 100.0


@patch("app.repository.table")
def test_create_order_failure(mock_table):
    repo = OrderRepository()
    order = OrderCreate(user_id="user1", amount=100.0)
    mock_table.put_item.side_effect = botocore.exceptions.BotoCoreError()
    with pytest.raises(Exception, match="Failed to create order"):
        repo.create_order(order)


@patch("app.repository.table")
def test_get_order_success(mock_table):
    repo = OrderRepository()
    mock_table.get_item.return_value = {
        "Item": {"order_id": "1", "user_id": "user1", "amount": 100.0}
    }
    result = repo.get_order("1")
    assert result["order_id"] == "1"


@patch("app.repository.table")
def test_get_order_failure(mock_table):
    repo = OrderRepository()
    mock_table.get_item.side_effect = botocore.exceptions.BotoCoreError()
    with pytest.raises(Exception, match="Failed to get order"):
        repo.get_order("1")
