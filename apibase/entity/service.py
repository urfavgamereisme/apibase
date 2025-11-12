from typing import Dict, Union, Any, List

from sqlalchemy import Table, insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


async def insert_entity(
    db_session: AsyncSession,
    table: Table, data: Dict[str, Any]
):
    query = insert(table).values(**data)
    await db_session.execute(query)
    await db_session.commit()


async def select_entity(
    db_session: AsyncSession,
    table: Table, entity_id: int = None
) -> List[Table]:
    if entity_id:
        query = select(table).where(table.c.id == entity_id)
    else:
        query = select(table)
    response = await db_session.execute(query)
    return response.all()


async def update_entity(
    db_session: AsyncSession,
    table: Table, entity_id: int,
    data: Dict[str, Any]
):
    query = (
        update(table)
        .where(table.c.id == entity_id)
        .values(**data)
        .returning(table)
    )
    await db_session.execute(query)
    await db_session.commit()


async def delete_entity(
    db_session: AsyncSession,
    table: Table, entity_id: int
):
    query = delete(table).where(table.c.id == entity_id)
    await db_session.execute(query)
    await db_session.commit()
