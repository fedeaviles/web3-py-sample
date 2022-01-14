from unittest.mock import patch
import pytest

from app.functions import *
from app.tests.fixtures import *


def test_create_product(mock_contract, mock_w3, account_1, mock_request):
    create_product("test_product", account_1.address)

    # get the created product
    created_product = get_product(0)

    assert created_product["name"] == "test_product"
    assert created_product["status"] == 0
    assert created_product["owner"] == account_1.address
    assert created_product["newOwner"] == "0x0000000000000000000000000000000000000000"


def test_get_product(mock_contract, mock_w3, account_1, new_product):
    product = get_product(0)

    assert product["name"] == "new_prod"
    assert product["status"] == 0
    assert product["owner"] == account_1.address
    assert product["newOwner"] == "0x0000000000000000000000000000000000000000"


def test_get_product_raise_exception(mock_contract, mock_w3):
    with pytest.raises(InvalidProductId):
        get_product(0)


@pytest.mark.parametrize("mock_products", [10], indirect=True)
def test_get_filtered_product_by_name(mock_contract, mock_w3, mock_products):
    products = get_filtered_products(name="prod_3")

    assert len(products) == 1
    assert products[0]["name"] == "prod_3"


@pytest.mark.parametrize("mock_products", [[10, "addr1", "addr2"]], indirect=True)
def test_get_filtered_product_by_owner(mock_contract, mock_w3, mock_products):

    products = get_filtered_products(owner="addr1")

    for i in range(0, len(products)):
        assert products[i]["owner"] == "addr1"

    assert len(products) == 5


@pytest.mark.parametrize("mock_products", [10], indirect=True)
def test_get_filtered_product_by_status(mock_contract, mock_w3, mock_products):
    products = get_filtered_products(status=0)

    for i in range(0, len(products)):
        assert products[i]["status"] == 0

    assert len(products) == 5


@pytest.mark.parametrize("mock_products", [[10, "addr1", "addr2"]], indirect=True)
def test_get_filtered_product_by_newOwner(mock_contract, mock_w3, mock_products):
    products = get_filtered_products(newOwner="addr1")

    for i in range(0, len(products)):
        assert products[i]["newOwner"] == "addr1"

    assert len(products) == 5


def test_account_cannot_create_more_than_eleven_products(
    mock_contract, mock_w3, account_1, mock_request
):
    for i in range(12):
        create_product("test_product", account_1.address)

    products = get_all_products()
    assert len(products) == 11


def test_delegate_product(
    mock_contract, mock_w3, account_1, account_2, mock_request, new_product
):
    # get the created product
    created_product = get_product(0)
    assert created_product["status"] == 0
    assert created_product["owner"] == account_1.address
    assert created_product["newOwner"] == "0x0000000000000000000000000000000000000000"

    delegate_product(0, account_1.address, account_2.address)

    # get the delegated product
    delegated_product = get_product(0)
    assert delegated_product["status"] == 1
    assert delegated_product["owner"] == account_1.address
    assert delegated_product["newOwner"] == account_2.address


@patch("app.functions.send_transaction")
@patch("app.functions.contract.functions.acceptProduct")
def test_accept_product(mock_accept, mock_send_tx):
    tx = "fake-tx"
    addr = "0x%040d" % 1
    mock_accept.return_value = tx
    accept_product(0, addr)
    mock_accept.assert_called_once_with(0)
    mock_send_tx.assert_called_once_with(tx, addr)


@pytest.mark.parametrize("new_product", [10], indirect=True)
def test_get_all_products(mock_contract, mock_w3, account_1, new_product):
    products = get_all_products()

    for i in range(0, len(products)):
        assert products[i]["name"] == "new_prod_" + str(i)
        assert products[i]["status"] == 0
        assert products[i]["owner"] == account_1.address
        assert products[i]["newOwner"] == "0x0000000000000000000000000000000000000000"

    assert len(products) == 10
