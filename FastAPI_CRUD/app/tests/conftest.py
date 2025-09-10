import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import async_session, Base, engine


@pytest.fixture(scope="session")
def event_loop():
    """Create a session-scoped event loop for async tests."""
    loop = asyncio.get_event_loop()
    yield loop


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """Set up the database once for the test session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    """Async client for making requests to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session():
    """Async DB session for tests."""
    async with async_session() as session:
        yield session
