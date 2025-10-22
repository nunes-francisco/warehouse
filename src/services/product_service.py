from typing import List, Optional
from src.repository.product_repository import ProductRepository
from src.schemas.product import ProductCreate, ProductUpdate
from src.domain.models import Product
import uuid


class ProductService:
    """ Service layer for managing Product entities. """
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """ Retrieve all products with pagination. """
        return await self.product_repository.get_all(skip=skip, limit=limit)

    async def create_product(self, product: ProductCreate) -> Product:
        """ Create a new product in the database. """
        return await self.product_repository.create(product=product)

    async def get_product(self, product_id: uuid.UUID) -> Optional[Product]:
        """ Retrieve a product by its ID. """
        return await self.product_repository.get(product_id=product_id)

    async def update_product(
        self, product_id: uuid.UUID, product: ProductUpdate
    ) -> Optional[Product]:
        """ Update an existing product in the database. """
        return await self.product_repository.update(
            product_id=product_id, product=product
        )

    async def delete_product(self, product_id: uuid.UUID) -> Optional[Product]:
        """ Delete a product from the database. """
        return await self.product_repository.delete(product_id=product_id)
