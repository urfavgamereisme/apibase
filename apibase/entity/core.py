import os
import json
from typing import Dict
from pathlib import Path

from sqlalchemy import MetaData, Table, Column, Integer, Float, Text


metadata = MetaData()


def init_entities(path: Path):
    tables = []
    
    if path.is_dir():
        entity_files = os.listdir(path)
        for filename in entity_files:
            file_path = path / filename
            with open(file_path, 'r') as f:
                entity = json.load(f)
            tables.append(create_table_from_entity(entity))
    return metadata
    

def create_table_from_entity(entity: Dict):
    types = {'text': Text, 'number': Float}
    name, attributes = entity.get('name'), entity.get('attributes')
    
    columns = [Column('id', Integer, primary_key=True)]
    for field, info in attributes.items():
        column_type = types.get(info.get('type'))
        columns.append(Column(field, column_type, nullable=True))
    return Table(name, metadata, *columns)
