"""Define a camada de serviço para a gestão de produtos."""

from typing import List, Optional
from src.repository.product_repository import ProductRepository
from src.schemas.product import ProductCreate, ProductUpdate
from src.domain.models import Product
import uuid


class ProductService:
    """Camada de serviço para gerenciar entidades de Produto."""

    def __init__(self, product_repository: ProductRepository):
        """Inicializa o serviço de produto com um repositório de produtos."""
        self.product_repository = product_repository

    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Recupera todos os produtos com paginação."""
        return await self.product_repository.get_all(skip=skip, limit=limit)

    async def create_product(self, product: ProductCreate) -> Product:
        """Cria um novo produto no banco de dados."""
        return await self.product_repository.create(product=product)

    async def get_product(self, product_id: uuid.UUID) -> Optional[Product]:
        """Recupera um produto pelo seu ID."""
        return await self.product_repository.get(product_id=product_id)

    async def update_product(
        self, product_id: uuid.UUID, product: ProductUpdate
    ) -> Optional[Product]:
        """Atualiza um produto existente no banco de dados."""
        return await self.product_repository.update(
            product_id=product_id, product=product
        )

    async def delete_product(self, product_id: uuid.UUID) -> Optional[Product]:
        """Exclui um produto do banco de dados."""
        return await self.product_repository.delete(product_id=product_id)
