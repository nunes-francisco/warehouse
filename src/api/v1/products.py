from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.schemas.product import Product, ProductCreate, ProductUpdate
from src.services.product_service import ProductService
from src.repository.product_repository import ProductRepository
import uuid

router = APIRouter()


def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    """ Retorna uma instância de ProductService com o repositório injetado. """
    product_repository = ProductRepository(session)
    return ProductService(product_repository)


@router.post("/", response_model=Product, status_code=201)
async def create_product(
    product: ProductCreate, service: ProductService = Depends(get_product_service)
):
    """ Cria um novo produto. E retorna o produto criado. """
    return await service.create_product(product=product)


@router.get("/", response_model=List[Product])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service),
):
    """ Retorna uma lista de produtos. """
    return await service.get_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=Product)
async def read_product(
    product_id: uuid.UUID, service: ProductService = Depends(get_product_service)
):
    """ Retorna um produto pelo ID. """
    db_product = await service.get_product(product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.patch("/{product_id}", response_model=Product)
async def update_product(
    product_id: uuid.UUID,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """ Atualiza um produto pelo ID. """
    db_product = await service.update_product(product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}", response_model=Product)
async def delete_product(
    product_id: uuid.UUID, service: ProductService = Depends(get_product_service)
):
    """ Deleta um produto pelo ID. """
    db_product = await service.delete_product(product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
