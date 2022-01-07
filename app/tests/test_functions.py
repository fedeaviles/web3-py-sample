import pytest
from app.functions import *

from app.tests.fixtures import *


def test_create_product(mock_contract, mock_w3, account_1):
    create_product("test_product", account_1.address, account_1.key)

    # get the created product
    created_product = get_product(0)

    assert created_product["name"] == "test_product"
    assert created_product["status"] == 0
    assert created_product["owner"] == account_1.address
    assert created_product["newOwner"] == "0x0000000000000000000000000000000000000000"


def test_get_product(mock_contract, mock_w3, account_1):
    create_product("test_product", account_1.address, account_1.key)

    product = get_product(0)

    assert product["name"] == "test_product"
    assert product["status"] == 0
    assert product["owner"] == account_1.address
    assert product["newOwner"] == "0x0000000000000000000000000000000000000000"


def test_get_product_raise_exception(mock_contract, mock_w3):
    with pytest.raises(InvalidProductId):
        get_product(0)


def test_get_filtered_product_by_name(mock_contract, mock_w3, account_1):
    create_product("test_product0", account_1.address, account_1.key)
    create_product("test_product1", account_1.address, account_1.key)

    products = get_filtered_products(name="test_product0")

    assert len(products) == 1
    assert products[0]["name"] == "test_product0"


def test_get_filtered_product_by_owner(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product0", account_1.address, account_1.key)
    create_product("test_product1", account_1.address, account_1.key)
    create_product("test_product2", account_2.address, account_2.key)

    products = get_filtered_products(owner=account_1.address)

    for i in range(0, len(products)):
        assert products[i]["owner"] == account_1.address

    assert len(products) == 2


def test_get_filtered_product_by_status(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product0", account_1.address, account_1.key)
    create_product("test_product1", account_1.address, account_1.key)

    delegate_product(0, account_1.address, account_1.key, account_2.address)

    products = get_filtered_products(status=0)

    assert products[0]["id"] == 1
    assert products[0]["status"] == 0

    assert len(products) == 1


def test_get_filtered_product_by_newOwner(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product0", account_1.address, account_1.key)
    create_product("test_product1", account_1.address, account_1.key)
    create_product("test_product2", account_2.address, account_2.key)

    delegate_product(0, account_1.address, account_1.key, account_2.address)

    products = get_filtered_products(newOwner=account_2.address)

    for i in range(0, len(products)):
        assert products[i]["newOwner"] == account_2.address

    assert len(products) == 1


def test_account_cannot_create_more_than_eleven_products(
    mock_contract, mock_w3, account_1
):
    for i in range(12):
        create_product("test_product", account_1.address, account_1.key)

    products = get_all_products()
    assert len(products) == 11


def test_delegate_product(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product", account_1.address, account_1.key)
    # get the created product
    created_product = get_product(0)
    assert created_product["status"] == 0
    assert created_product["owner"] == account_1.address
    assert created_product["newOwner"] == "0x0000000000000000000000000000000000000000"

    delegate_product(0, account_1.address, account_1.key, account_2.address)

    # get the delegated product
    delegated_product = get_product(0)
    assert delegated_product["status"] == 1
    assert delegated_product["owner"] == account_1.address
    assert delegated_product["newOwner"] == account_2.address


def test_accept_product(mock_contract, mock_w3, account_1, account_2):
    create_product("test_product", account_1.address, account_1.key)

    delegate_product(0, account_1.address, account_1.key, account_2.address)
    # get the delegated product
    delegated_product = get_product(0)
    assert delegated_product["status"] == 1
    assert delegated_product["owner"] == account_1.address
    assert delegated_product["newOwner"] == account_2.address

    accept_product(0, account_2.address, account_2.key)

    # get the accepted product
    accepted_product = get_product(0)

    assert accepted_product["status"] == 0
    assert accepted_product["owner"] == account_2.address
    assert accepted_product["newOwner"] == "0x0000000000000000000000000000000000000000"


def test_get_all_products(mock_contract, mock_w3, account_1):
    create_product("test_product0", account_1.address, account_1.key)
    create_product("test_product1", account_1.address, account_1.key)

    products = get_all_products()

    for i in range(0, len(products)):
        assert products[i]["name"] == "test_product" + str(i)
        assert products[i]["status"] == 0
        assert products[i]["owner"] == account_1.address
        assert products[i]["newOwner"] == "0x0000000000000000000000000000000000000000"

    assert len(products) == 2


def test_get_delegated_products(
    mock_contract, mock_w3, mock_first_block, account_1, account_2
):
    create_product("test_product0", account_1.address, account_1.key)
    create_product("test_product1", account_1.address, account_1.key)

    delegate_product(0, account_1.address, account_1.key, account_2.address)

    delegated_products = get_delegated_products()

    assert len(delegated_products) == 1

    assert delegated_products[0]["args"]["productId"] == 0
    assert delegated_products[0]["args"]["newOwner"] == account_2.address
    assert delegated_products[0]["args"]["status"] == 1


def test_get_accepted_products(
    mock_contract, mock_w3, mock_first_block, account_1, account_2
):
    create_product("test_product0", account_1.address, account_1.key)
    create_product("test_product1", account_1.address, account_1.key)

    delegate_product(0, account_1.address, account_1.key, account_2.address)
    accept_product(0, account_2.address, account_2.key)

    accepted_products = get_accepted_products()

    assert len(accepted_products) == 1

    assert accepted_products[0]["args"]["productId"] == 0
    assert accepted_products[0]["args"]["status"] == 0
