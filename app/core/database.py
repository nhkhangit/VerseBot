# app/core/database.py
import asyncpg
from fastapi import Request
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

async def get_connection(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    """Get database connection from pool stored in app state"""
    async with request.app.state.pool.acquire() as conn:
        yield conn