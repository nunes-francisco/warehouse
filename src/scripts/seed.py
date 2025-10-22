"""Script para popular o banco de dados com dados de exemplo."""

import asyncio
from faker import Faker
from src.core.database import async_session
from src.domain.models import Product
from sqlalchemy.dialects.postgresql import insert

fake = Faker()


async def seed_data():
    """Popula o banco de dados com dados de produtos de exemplo."""
    async with async_session() as session:  # type: AsyncSession
        products = []
        for _ in range(100):
            products.append(
                {
                    "name": fake.name(),
                    "description": fake.text(),
                    "price": fake.random_number(digits=2),
                    "in_stock": fake.boolean(),
                }
            )

        await session.execute(insert(Product), products)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_data())
