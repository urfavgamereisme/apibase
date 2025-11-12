from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends

from apibase.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session():
    async with session_factory() as session:
        yield session

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
