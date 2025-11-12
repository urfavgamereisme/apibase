from pathlib import Path

DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'

ENTITIES_PATH = Path(__file__).resolve().parent.parent / 'entity_schemas'