import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)
from src.domain.models import Product
from src.schemas.product import ProductCreate

@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, app: FastAPI):
    """Testa a criação de um novo produto."""
    product = ProductCreate(name="Test Product", price=10.0)
    response = await client.post(
        app.url_path_for("create_product"), json=product.model_dump()
    )
    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    assert data["name"] == product.name
    assert data["price"] == product.price


@pytest.mark.asyncio
async def test_get_products(client: AsyncClient, app: FastAPI, test_product: Product):
    """Testa a busca por todos os produtos."""
    response = await client.get(app.url_path_for("read_products"))
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_product(client: AsyncClient, app: FastAPI, test_product: Product):
    """Testa a busca por um único produto pelo seu ID."""
    response = await client.get(
        app.url_path_for("read_product", product_id=str(test_product.id))
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["id"] == str(test_product.id)


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient, app: FastAPI):
    """Testa a busca por um produto inexistente."""
    import uuid

    response = await client.get(
        app.url_path_for("read_product", product_id=str(uuid.uuid4()))
    )
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, app: FastAPI, test_product: Product):
    """Testa a atualização de um produto existente."""
    updated_product = {"name": "Updated Test Product"}
    response = await client.patch(
        app.url_path_for("update_product", product_id=str(test_product.id)),
        json=updated_product,
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["name"] == updated_product["name"]


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, app: FastAPI, test_product: Product):
    """Testa a exclusão de um produto."""
    response = await client.delete(
        app.url_path_for("delete_product", product_id=str(test_product.id))
    )
    assert response.status_code == HTTP_200_OK
    response = await client.get(
        app.url_path_for("read_product", product_id=str(test_product.id))
    )
    assert response.status_code == HTTP_404_NOT_FOUND
