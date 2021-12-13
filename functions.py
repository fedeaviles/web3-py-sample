from settings import w3, contract, first_block

def create_product(name, address, private_key):
    tx = contract.functions.createProduct(name).buildTransaction(
        {
            'from': address,
            'nonce': w3.eth.getTransactionCount(address),
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei')
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    return w3.eth.send_raw_transaction(signed_tx.rawTransaction)

def delegate_product(product_id, from_address, from_private_key, to_address):
    tx = contract.functions.delegateProduct(product_id, to_address).buildTransaction(
        {
            'from': from_address,
            'nonce': w3.eth.getTransactionCount(from_address),
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei')
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, from_private_key)
    return w3.eth.send_raw_transaction(signed_tx.rawTransaction)

def accept_product(product_id, address, private_key):
    tx = contract.functions.acceptProduct(product_id).buildTransaction(
        {
            'from': address,
            'nonce': w3.eth.getTransactionCount(address),
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei')
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    return w3.eth.send_raw_transaction(signed_tx.rawTransaction)

def get_product(product_id):
    return contract.functions.products(product_id).call()

def get_all_products():
    new_product_event_filter = contract.events.NewProduct.createFilter(fromBlock=first_block)
    all_products = new_product_event_filter.get_all_entries()
    return all_products

def get_product_by_name(name):
    new_product_event_filter = contract.events.NewProduct.createFilter(fromBlock=first_block, argument_filters={'name': name})
    all_products = new_product_event_filter.get_all_entries()
    return all_products

def get_delegated_products():
    delegated_product_event_filter = contract.events.DelegateProduct.createFilter(fromBlock=first_block)
    all_products = delegated_product_event_filter.get_all_entries()
    return all_products

def get_delegated_products_by_owner(new_owner):
    delegated_product_event_filter = contract.events.DelegateProduct.createFilter(fromBlock=first_block, argument_filters={'newOwner': new_owner})
    all_products = delegated_product_event_filter.get_all_entries()
    return all_products

def get_accepted_products():
    accepted_product_event_filter = contract.events.AcceptProduct.createFilter(fromBlock=first_block)
    all_products = accepted_product_event_filter.get_all_entries()
    return all_products