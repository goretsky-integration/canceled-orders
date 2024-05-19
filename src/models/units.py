from uuid import UUID

from pydantic import BaseModel

__all__ = ('Unit',)


class Unit(BaseModel):
    id: int
    name: str
    uuid: UUID
    account_name: str
