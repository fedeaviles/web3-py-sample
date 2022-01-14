from fastapi import FastAPI, HTTPException
from pydantic import NonNegativeInt, BaseModel
from app.exceptions import InvalidProductId
import app.functions as functions

app = FastAPI()


class ProductCreate(BaseModel):
    name: str
    address: str


class ProductDelegate(BaseModel):
    address: str
    new_address: str


class ProductAccept(BaseModel):
    address: str


@app.get("/products")
async def read_products():
    return functions.get_all_products()


@app.get("/products/{id}")
async def read_product(id: NonNegativeInt):
    try:
        return functions.get_product(id)
    except (InvalidProductId):
        raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
async def create_product(product: ProductCreate):
    try:
        tx = functions.create_product(product.name, product.address)
        return {"transaction_hash": tx.hex()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/products/{id}/delegate")
async def delegate_product(id: int, product: ProductDelegate):
    try:
        tx = functions.delegate_product(id, product.address, product.new_address)
        return {"transaction_hash": tx.hex()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/products/{id}/accept")
async def accept_product(id: int, product: ProductAccept):
    try:
        tx = functions.accept_product(id, product.address)
        return {"transaction_hash": tx.hex()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
