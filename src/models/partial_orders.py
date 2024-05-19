from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = (
    'PartialOrder',
    'PartialOrdersResponsePagination',
    'PartialOrdersResponse',
)


class PartialOrder(BaseModel):
    id: Annotated[UUID, Field(alias='Id')]


class PartialOrdersResponsePagination(BaseModel):
    current_page: Annotated[int, Field(alias='CurrentPage')]
    next_page: Annotated[int | None, Field(alias='NextPage')]
    per_page: Annotated[int, Field(alias='PerPage')]
    prev_page: Annotated[int | None, Field(alias='PrevPage')]
    total_pages: Annotated[int, Field(alias='TotalPages')]
    total_records: Annotated[int, Field(alias='TotalRecords')]


class PartialOrdersResponse(BaseModel):
    items: Annotated[list[PartialOrder], Field(alias='Items')]
    pagination: Annotated[
        PartialOrdersResponsePagination,
        Field(alias='Pagination'),
    ]
