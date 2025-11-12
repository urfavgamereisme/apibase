from typing import Dict, Union

from sqlalchemy import Text, Float


def validate_entity(data: Dict, entity_table) -> bool:
    types = {Text: str, Float: Union[float, int]}
    columns = list(entity_table.columns)
    column_schema = {}
    for column in columns:
        if column.name == 'id':
            continue
        column_type = types.get(type(column.type))
        column_schema.update({column.name: column_type})

    for key, value in data.items():
        if key not in column_schema.keys():
            return False
        if not isinstance(value, column_schema.get(key)):
            return False
    return True
