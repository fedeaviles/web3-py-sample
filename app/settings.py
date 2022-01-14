import json, os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(
    Web3.HTTPProvider(
        os.getenv("NODE_URL", "https://matic-testnet-archive-rpc.bwarelabs.com")
    )
)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

abi = json.loads(
    '[{"constant":false,"inputs":[{"name":"_name","type":"string"}],"name":"createProduct","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"productToOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_productId","type":"uint256"},{"name":"_newOwner","type":"address"}],"name":"delegateProduct","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_productId","type":"uint256"}],"name":"acceptProduct","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"products","outputs":[{"name":"name","type":"string"},{"name":"status","type":"uint8"},{"name":"owner","type":"address"},{"name":"newOwner","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"size","outputs":[{"name":"count","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"productId","type":"uint256"},{"indexed":false,"name":"name","type":"string"}],"name":"NewProduct","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"productId","type":"uint256"},{"indexed":false,"name":"newOwner","type":"address"},{"indexed":false,"name":"status","type":"uint8"}],"name":"DelegateProduct","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"productId","type":"uint256"},{"indexed":false,"name":"name","type":"string"},{"indexed":false,"name":"status","type":"uint8"}],"name":"AcceptProduct","type":"event"}]'
)
contract_address = w3.toChecksumAddress("0xd9E0b2C0724F3a01AaECe3C44F8023371f845196")
contract = w3.eth.contract(address=contract_address, abi=abi)

sign_url = os.getenv("SIGN_URL")

minimum_confirmations = int(os.getenv("MINIMUM_CONFIRMATIONS", "10"))
