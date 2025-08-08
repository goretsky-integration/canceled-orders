from uuid import UUID

from pydantic import BaseModel, Field

from enums import CountryCode, SalesChannel

__all__ = ('EventPayload', 'Event', 'EventPayloadOrder')


class EventPayloadOrder(BaseModel):
    id: UUID
    number: str
    price: int
    sales_channel: SalesChannel
    is_refund_receipt_printed: bool


class EventPayload(BaseModel):
    unit_name: str
    orders: list[EventPayloadOrder]
    country_code: CountryCode


class Event(BaseModel):
    unit_ids: list[int]
    type: str = Field(default='CANCELED_ORDERS', frozen=True)
    payload: EventPayload
