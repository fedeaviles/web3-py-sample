from unittest.mock import patch
from hexbytes import HexBytes
from fastapi.testclient import TestClient

from main import app
from app.functions import (
    create_product,
    delegate_product,
    get_all_products,
    get_product,
)
from app.tests.fixtures import *
from app.exceptions import InvalidProductId


client = TestClient(app)


@patch("app.functions.create_product")
def test_create_product(mock_create):
    hex = HexBytes("0x000546512314847856")
    mock_create.return_value = hex
    response = client.post(
        "/products",
        json={
            "name": "test_product",
            "address": "0x0000000000000000000000000000000000000001",
        },
    )

    assert response.status_code == 200
    assert "transaction_hash" in response.json()
    assert response.json()["transaction_hash"] == hex.hex()


@patch("app.functions.create_product")
def test_create_product_error(mock_create):
    mock_create.side_effect = Exception("Error")
    response = client.post(
        "/products",
        json={
            "name": "test_product",
            "address": "0",
        },
    )
    assert response.status_code == 400


@patch("app.functions.get_product")
def test_read_product(mock_get_product):
    prod_data = {
        "id": 0,
        "name": "test_product_0",
        "status": 0,
        "owner": "0x0000000000000000000000000000000000000001",
        "newOwner": "0x0000000000000000000000000000000000000000",
    }
    mock_get_product.return_value = prod_data

    response = client.get("/products/0")
    assert response.status_code == 200
    assert response.json() == prod_data
    mock_get_product.assert_called_once_with(0)


@patch("app.functions.get_product")
def test_read_product_raise_exception(mock_get_product):
    mock_get_product.side_effect = InvalidProductId("Product not found")
    response = client.get("/products/0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


@patch("app.functions.get_all_products")
def test_read_products(mock_get_all_products):
    prods_data = [
        {
            "id": 0,
            "name": "test_product_0",
            "status": 0,
            "owner": "0x0000000000000000000000000000000000000001",
            "newOwner": "0x0000000000000000000000000000000000000000",
        },
        {
            "id": 1,
            "name": "test_product_1",
            "status": 0,
            "owner": "0x0000000000000000000000000000000000000001",
            "newOwner": "0x0000000000000000000000000000000000000000",
        },
    ]
    mock_get_all_products.return_value = prods_data
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == prods_data


@patch("app.functions.delegate_product")
def test_delegate_product(mock_delegate):
    hex = HexBytes("0x000546512314847856")
    mock_delegate.return_value = hex

    response = client.post(
        "/products/0/delegate",
        json={
            "address": "0x0000000000000000000000000000000000000001",
            "new_address": "0x0000000000000000000000000000000000000002",
        },
    )
    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.json()["transaction_hash"] == hex.hex()


@patch("app.functions.delegate_product")
def test_delegate_product_error(mock_delegate):
    mock_delegate.side_effect = Exception("Error")
    response = client.post(
        "/products/0/delegate",
        json={
            "address": "0",
            "new_address": "0",
        },
    )
    assert response.status_code == 400


@patch("app.functions.accept_product")
def test_accept_product(mock_accept):
    hex = HexBytes("0x000546512314847856")
    mock_accept.return_value = hex

    response = client.post(
        "/products/0/accept",
        json={
            "address": "0x0000000000000000000000000000000000000001",
            "key": "0x0000000000000000000000000000000000000002",
        },
    )
    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.json()["transaction_hash"] == hex.hex()


@patch("app.functions.accept_product")
def test_accept_product_error(mock_accept):
    mock_accept.side_effect = Exception("Error")
    response = client.post(
        "/products/0/accept",
        json={
            "address": "0",
            "key": "0",
        },
    )
    assert response.status_code == 400
