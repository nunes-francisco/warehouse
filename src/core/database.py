"""Configura a conexão com o banco de dados e gerencia sessões assíncronas."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.settings import settings

engine = create_async_engine(settings.DATABASE_URL_LOCAL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Retorna uma sessão assíncrona do banco de dados."""
    async with async_session() as session:
        yield session
