from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.models import Product
from src.schemas.product import ProductCreate, ProductUpdate
import uuid


class ProductRepository:
    """Repositório para gerenciar entidades de Produto no banco de dados."""

    def __init__(self, session: AsyncSession):
        """Inicializa o repositório com uma sessão assíncrona."""
        self.session = session

    async def get(self, product_id: uuid.UUID) -> Optional[Product]:
        """Recupera um produto pelo seu ID."""
        result = await self.session.execute(
            select(Product).filter(Product.id == product_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Recupera todos os produtos com paginação."""
        result = await self.session.execute(select(Product).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, product: ProductCreate) -> Product:
        """Cria um novo produto no banco de dados."""
        db_product = Product(**product.model_dump())
        self.session.add(db_product)
        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product

    async def update(
        self, product_id: uuid.UUID, product: ProductUpdate
    ) -> Optional[Product]:
        """Atualiza um produto existente no banco de dados."""
        db_product = await self.get(product_id)
        if db_product:
            update_data = product.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_product, key, value)
            await self.session.commit()
            await self.session.refresh(db_product)
        return db_product

    async def delete(self, product_id: uuid.UUID) -> Optional[Product]:
        """Exclui um produto do banco de dados."""
        db_product = await self.get(product_id)
        if db_product:
            await self.session.delete(db_product)
            await self.session.commit()
        return db_product
