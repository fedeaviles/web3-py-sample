import json, os

from unittest.mock import patch
from fastapi.testclient import TestClient
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes

from service import app
from app.tests.fixtures import mock_env_key

client = TestClient(app)


@patch("service.w3.eth.account.sign_transaction")
def test_sign_tx(mock_sign_transaction, mock_env_key):
    rawTransaction = HexBytes("0x" + "2" * 64)
    hash = HexBytes("0x" + "3" * 64)
    r = 444444444
    s = 555555555
    v = 6666666
    mock_sign_transaction.return_value = SignedTransaction(
        rawTransaction=rawTransaction,
        hash=hash,
        r=r,
        s=s,
        v=v,
    )
    json_tx = json.dumps(
        {
            "value": 0,
            "chainId": 61,
            "from": "0x1dFD4c3b39AFd67c6F9E38cd3a2AC94A4Aea0691",
            "nonce": 0,
            "gas": 2000000,
            "gasPrice": 40000000000,
            "to": "0xF2E246BB76DF876Cef8b38ae84130F4F55De395b",
            "data": "0x02ec06be0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000c746573745f70726f647563740000000000000000000000000000000000000000",
        }
    )
    response = client.post("/", json=json_tx)

    mock_sign_transaction.assert_called_once_with(
        json.loads(json_tx), os.environ["KEY"]
    )
    assert response.status_code == 200
    assert response.json()["rawTransaction"] == rawTransaction.hex()
    assert response.json()["hash"] == hash.hex()
    assert response.json()["r"] == r
    assert response.json()["s"] == s
    assert response.json()["v"] == v


@patch("service.w3.eth.account.sign_transaction")
def test_sign_tx_raise_exception(mock_sign_transaction, mock_env_key):
    mock_sign_transaction.side_effect = Exception("test")
    json_tx = json.dumps(
        {
            "value": 0,
            "chainId": 61,
            "from": "0x1dFD4c3b39AFd67c6F9E38cd3a2AC94A4Aea0691",
            "nonce": 0,
            "gas": 2000000,
            "gasPrice": 40000000000,
            "to": "0xF2E246BB76DF876Cef8b38ae84130F4F55De395b",
            "data": "0x02ec06be0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000c746573745f70726f647563740000000000000000000000000000000000000000",
        }
    )
    response = client.post("/", json=json_tx)

    assert response.status_code == 400
    assert response.json()["detail"] == "test"
