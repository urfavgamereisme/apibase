from typing import Dict, Annotated, Union

from sqlalchemy import Table
from fastapi import APIRouter, HTTPException, Body

from .core import metadata
from .utils import validate_entity
from .service import insert_entity, select_entity, update_entity, delete_entity
from apibase.database import DbSession


router = APIRouter()

Data = Annotated[Dict[str, Union[str, float, int]], Body()]


@router.post('/api/entities/{entity}')
async def create_entity_handler(
    entity: str, data: Data, db_session: DbSession
):
    entity_table = metadata.tables.get(entity)
    if not isinstance(entity_table, Table):
        raise HTTPException(
            status_code=404,
            detail='Entity table not found'
        )
    
    if not validate_entity(data, entity_table):
        raise HTTPException(
            status_code=400
        )

    await insert_entity(db_session, entity_table, data)
    return {'detail': 'Done'}


@router.get('/api/entities/{entity}')
async def get_entities_handler(entity: str, db_session: DbSession):
    entity_table = metadata.tables.get(entity)
    if not isinstance(entity_table, Table):
        raise HTTPException(
            status_code=404,
            detail='Entity table not found'
        )
    entities = await select_entity(db_session, entity_table)
    entities = [list(e) for e in entities]
    return {'entities': entities}


@router.get('/api/entities/{entity}/{entity_id}')
async def get_entity_handler(entity: str, entity_id: int, db_session: DbSession):
    entity_table = metadata.tables.get(entity)
    if not isinstance(entity_table, Table):
        raise HTTPException(
            status_code=404,
            detail='Entity table not found'
        )
    entity = await select_entity(db_session, entity_table, entity_id)
    entity = list(entity[0]) if entity else []
    return {'entity': entity}


@router.put('/api/entities/{entity}/{entity_id}')
async def update_entity_handler(entity: str, entity_id: int, data: Data, db_session: DbSession):
    entity_table = metadata.tables.get(entity)
    if not isinstance(entity_table, Table):
        raise HTTPException(
            status_code=404,
            detail='Entity table not found'
        )
    
    if not validate_entity(data, entity_table):
        raise HTTPException(
            status_code=400
        )

    await update_entity(db_session, entity_table, entity_id, data)
    return {'detail': 'Done'}


@router.delete('/api/entities/{entity}/{entity_id}')
async def delete_entity_handler(entity: str, entity_id: int, db_session: DbSession):
    entity_table = metadata.tables.get(entity)
    if not isinstance(entity_table, Table):
        raise HTTPException(
            status_code=404,
            detail='Entity table not found'
        )
    await delete_entity(db_session, entity_table, entity_id)
    return {'detail': 'Done'}