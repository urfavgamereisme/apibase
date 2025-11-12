import asyncio

from fastapi import FastAPI

from apibase.database import engine
from apibase.config import ENTITIES_PATH
from apibase.entity.core import init_entities

from apibase.entity.router import router as entity_router


app = FastAPI()


app.include_router(entity_router)


@app.on_event('startup')
async def startup():
    metadata = await asyncio.to_thread(init_entities, ENTITIES_PATH)
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)