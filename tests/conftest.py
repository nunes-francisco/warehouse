import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.database import get_session
from src.domain.models import Base, Product
from main import app as main_app

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def override_get_session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    os.remove("test.db")


@pytest.fixture
def app() -> FastAPI:
    main_app.dependency_overrides[get_session] = override_get_session
    return main_app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_product(session: AsyncSession) -> Product:
    product = Product(name="Test Product", price=10.0)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session
