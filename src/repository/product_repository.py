from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.models import Product
from src.schemas.product import ProductCreate, ProductUpdate
import uuid


class ProductRepository:
    """Repository for managing Product entities in the database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, product_id: uuid.UUID) -> Optional[Product]:
        """ Retrieve a product by its ID. """
        result = await self.session.execute(
            select(Product).filter(Product.id == product_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """ Retrieve all products with pagination. """
        result = await self.session.execute(select(Product).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, product: ProductCreate) -> Product:
        """ Create a new product in the database. """
        db_product = Product(**product.model_dump())
        self.session.add(db_product)
        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product

    async def update(
        self, product_id: uuid.UUID, product: ProductUpdate
    ) -> Optional[Product]:
        """ Update an existing product in the database. """
        db_product = await self.get(product_id)
        if db_product:
            update_data = product.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_product, key, value)
            await self.session.commit()
            await self.session.refresh(db_product)
        return db_product

    async def delete(self, product_id: uuid.UUID) -> Optional[Product]:
        """ Delete a product from the database. """
        db_product = await self.get(product_id)
        if db_product:
            await self.session.delete(db_product)
            await self.session.commit()
        return db_product
