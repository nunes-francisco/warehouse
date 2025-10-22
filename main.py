from fastapi import FastAPI
from src.api.v1 import products

app = FastAPI()

app.include_router(products.router, prefix="/api/v1/products", tags=["products"])


@app.get("/")
def read_root():
    """ Root endpoint returning a welcome message. """
    return {"message": "Welcome to the Products API"}
