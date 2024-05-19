import pathlib
from typing import Final

from pydantic import TypeAdapter

from models import Unit

__all__ = ('load_units',)

UNITS_FILE_PATH: Final[pathlib.Path] = (
        pathlib.Path(__file__).parent.parent / 'units.json'
)


def load_units(file_path: pathlib.Path = UNITS_FILE_PATH) -> list[Unit]:
    units_json = file_path.read_text(encoding='utf-8')
    type_adapter = TypeAdapter(list[Unit])
    return type_adapter.validate_json(units_json)
