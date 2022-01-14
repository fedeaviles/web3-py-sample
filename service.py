import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from pydantic import Json

from app.settings import w3

app = FastAPI()

load_dotenv()


@app.post("/")
async def sign_tx(tx: Json = Body(...)):
    key = os.environ["KEY"]
    try:
        signed_tx = w3.eth.account.sign_transaction(tx, key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.args[0]))
    return {
        "rawTransaction": signed_tx["rawTransaction"].hex(),
        "hash": signed_tx["hash"].hex(),
        "r": signed_tx["r"],
        "s": signed_tx["s"],
        "v": signed_tx["v"],
    }
