from app.settings import w3, contract, first_block
from app.exceptions import InvalidProductId


def send_transaction(transaction, address, private_key):
    tx = transaction.buildTransaction(
        {
            "from": address,
            "nonce": w3.eth.get_transaction_count(address),
            "gas": 2000000,
            "gasPrice": w3.toWei("40", "gwei"),
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    return w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def create_product(name, address, private_key):
    transaction = contract.functions.createProduct(name)
    return send_transaction(transaction, address, private_key)


def delegate_product(product_id, from_address, from_private_key, to_address):
    transaction = contract.functions.delegateProduct(product_id, to_address)
    return send_transaction(transaction, from_address, from_private_key)


def accept_product(product_id, address, private_key):
    transaction = contract.functions.acceptProduct(product_id)
    return send_transaction(transaction, address, private_key)


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


def get_product_by_name(name):
    new_product_event_filter = contract.events.NewProduct.createFilter(
        fromBlock=first_block, argument_filters={"name": name}
    )
    all_products = new_product_event_filter.get_all_entries()
    return all_products


def get_delegated_products():
    delegated_product_event_filter = contract.events.DelegateProduct.createFilter(
        fromBlock=first_block
    )
    all_products = delegated_product_event_filter.get_all_entries()
    return all_products


def get_delegated_products_by_owner(new_owner):
    delegated_product_event_filter = contract.events.DelegateProduct.createFilter(
        fromBlock=first_block, argument_filters={"newOwner": new_owner}
    )
    all_products = delegated_product_event_filter.get_all_entries()
    return all_products


def get_accepted_products():
    accepted_product_event_filter = contract.events.AcceptProduct.createFilter(
        fromBlock=first_block
    )
    all_products = accepted_product_event_filter.get_all_entries()
    return all_products
