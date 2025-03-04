from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncGenerator, Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.core.settings import get_settings
from src.core.mocks import get_database_session
from .base import Base

AsyncSessionGenerator = AsyncGenerator[AsyncSession, None]


async def create_database(url: str) -> None:
    engine = create_async_engine(
        url, pool_pre_ping=True, future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


async def delete_database(url: str) -> None:
    engine = create_async_engine(
        url, pool_pre_ping=True, future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


def async_session(
    url: str, *, wrap: Callable[..., Any] | None = None,
) -> Callable[..., AsyncSessionGenerator] | AsyncContextManager[Any]:
    engine = create_async_engine(
        url, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False,
    )

    async def get_session() -> AsyncSessionGenerator:  # noqa: WPS430, WPS442
        async with factory() as session:
            yield session

    return get_session if wrap is None else wrap(get_session)


def sync_session(url: str) -> orm.scoped_session:
    engine = create_engine(
        url, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, autoflush=False, expire_on_commit=False,
    )
    return orm.scoped_session(factory)


override_session = get_database_session, async_session(
    get_settings().database_uri)
current_session = sync_session(get_settings().database_uri
                               .replace('+asyncpg', ''))
context_session = async_session(get_settings()
                                .database_uri, wrap=asynccontextmanager)
testing_session = async_session(get_settings().test_database_uri)
