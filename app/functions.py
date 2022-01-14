import requests, json

from app.settings import w3, contract, sign_url
from app.exceptions import InvalidProductId


def send_transaction(transaction, address):
    tx = transaction.buildTransaction(
        {
            "from": address,
            "nonce": w3.eth.get_transaction_count(address),
            "gas": 2000000,
            "gasPrice": w3.toWei("40", "gwei"),
        }
    )
    # sign trough service
    signed_tx = requests.request(
        "POST",
        sign_url,
        headers={"content-type": "application/json"},
        json=json.dumps(tx),
    ).json()
    return w3.eth.send_raw_transaction(signed_tx["rawTransaction"])


def create_product(name, address):
    transaction = contract.functions.createProduct(name)
    return send_transaction(transaction, address)


def delegate_product(product_id, from_address, to_address):
    transaction = contract.functions.delegateProduct(product_id, to_address)
    return send_transaction(transaction, from_address)


def accept_product(product_id, address):
    transaction = contract.functions.acceptProduct(product_id)
    return send_transaction(transaction, address)


def get_product(product_id):
    products_count = contract.functions.size().call()
    if product_id < products_count:
        product = contract.functions.products(product_id).call()
        return {
            "id": product_id,
            "name": product[0],
            "status": product[1],
            "owner": product[2],
            "newOwner": product[3],
        }
    else:
        raise InvalidProductId("Product id is invalid")


def get_all_products():
    products_count = contract.functions.size().call()
    all_products = []
    for i in range(products_count):
        all_products.append(get_product(i))
    return all_products


def get_filtered_products(**kwargs):
    valid_filters = ["name", "status", "owner", "newOwner"]
    all_products = get_all_products()
    products = []
    for product in all_products:
        if all(
            key in valid_filters and product[key] == value
            for key, value in kwargs.items()
        ):
            products.append(product)
    return products
