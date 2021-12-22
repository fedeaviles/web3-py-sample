from fastapi.testclient import TestClient
from main import app
from app.functions import (
    create_product,
    delegate_product,
    get_all_products,
    get_product,
)
from app.tests.fixtures import *

client = TestClient(app)


def test_create_product(mock_contract, mock_w3, account_1):
    all_products = get_all_products()
    assert len(all_products) == 0

    response = client.post(
        "/products",
        json={
            "name": "test_product",
            "address": account_1.address,
            "key": account_1.key.hex(),
        },
    )

    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.json()["transaction_hash"].startswith("0x")

    all_products = get_all_products()
    assert len(all_products) == 1
    assert all_products[0]["name"] == "test_product"


def test_create_product_invalid_address(mock_contract, mock_w3, account_1):
    response = client.post(
        "/products",
        json={
            "name": "test_product",
            "address": "0",
            "key": account_1.key.hex(),
        },
    )
    assert response.status_code == 400


def test_create_product_invalid_key(mock_contract, mock_w3, account_1):
    response = client.post(
        "/products",
        json={
            "name": "test_product",
            "address": account_1.address,
            "key": "0",
        },
    )
    assert response.status_code == 400


def test_read_product(mock_contract, mock_w3, account_1):
    create_product("test_product_0", account_1.address, account_1.key)

    response = client.get("/products/0")
    assert response.status_code == 200
    assert response.json() == {
        "id": 0,
        "name": "test_product_0",
        "status": 0,
        "owner": account_1.address,
        "newOwner": "0x0000000000000000000000000000000000000000",
    }


def test_read_product_raise_exception(mock_contract, mock_w3):
    response = client.get("/products/0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_read_products(mock_contract, mock_w3, account_1):
    create_product("test_product_0", account_1.address, account_1.key)
    create_product("test_product_1", account_1.address, account_1.key)

    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 0,
            "name": "test_product_0",
            "status": 0,
            "owner": account_1.address,
            "newOwner": "0x0000000000000000000000000000000000000000",
        },
        {
            "id": 1,
            "name": "test_product_1",
            "status": 0,
            "owner": account_1.address,
            "newOwner": "0x0000000000000000000000000000000000000000",
        },
    ]


def test_delegate_product(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)

    response = client.post(
        "/products/0/delegate",
        json={
            "address": account_1.address,
            "key": account_1.key.hex(),
            "new_address": account_2.address,
        },
    )
    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.json()["transaction_hash"].startswith("0x")

    product = get_product(0)
    assert product["status"] == 1
    assert product["newOwner"] == account_2.address


def test_delegate_product_invalid_address(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)

    response = client.post(
        "/products/0/delegate",
        json={
            "address": "0",
            "key": account_1.key.hex(),
            "new_address": account_2.address,
        },
    )
    assert response.status_code == 400


def test_delegate_product_invalid_key(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)

    response = client.post(
        "/products/0/delegate",
        json={
            "address": account_1.address,
            "key": "0",
            "new_address": account_2.address,
        },
    )
    assert response.status_code == 400


def test_delegate_product_invalid_new_address(
    mock_contract, mock_w3, account_1, account_2
):
    create_product("test_product_0", account_1.address, account_1.key)

    response = client.post(
        "/products/0/delegate",
        json={
            "address": account_1.address,
            "key": account_1.key.hex(),
            "new_address": "0",
        },
    )
    assert response.status_code == 400


def test_accept_product(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)
    delegate_product(0, account_1.address, account_1.key, account_2.address)

    response = client.post(
        "/products/0/accept",
        json={
            "address": account_2.address,
            "key": account_2.key.hex(),
        },
    )
    assert response.status_code == 200
    # returns a valid transaction hash
    assert response.json()["transaction_hash"].startswith("0x")

    product = get_product(0)
    assert product["status"] == 0
    assert product["owner"] == account_2.address


def test_accept_product_invalid_address(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)
    delegate_product(0, account_1.address, account_1.key, account_2.address)

    response = client.post(
        "/products/0/accept",
        json={
            "address": "0",
            "key": account_2.key.hex(),
        },
    )
    assert response.status_code == 400


def test_accept_product_invalid_key(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product_0", account_1.address, account_1.key)
    delegate_product(0, account_1.address, account_1.key, account_2.address)

    response = client.post(
        "/products/0/accept",
        json={
            "address": account_2.address,
            "key": "0",
        },
    )
    assert response.status_code == 400
