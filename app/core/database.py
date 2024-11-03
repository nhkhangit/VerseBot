import asyncpg
from .config import get_settings
from typing import AsyncGenerator

async def get_pool() -> asyncpg.Pool:
    settings = get_settings()
    return await asyncpg.create_pool(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB
    )

async def get_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    async with app.state.pool.acquire() as conn:
        yield conn