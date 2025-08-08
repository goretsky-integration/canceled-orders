from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Protocol, TypeVar

import structlog.stdlib

from enums import CountryCode
from models.detailed_orders import DetailedOrder
from models.events import Event, EventPayload, EventPayloadOrder
from models.units import Unit


__all__ = ('group_by_account_name',)

logger = structlog.stdlib.get_logger('app')


class HasAccountName(Protocol):
    account_name: str


HasAccountNameT = TypeVar('HasAccountNameT', bound=HasAccountName)


def group_by_account_name(
        items: Iterable[HasAccountNameT],
) -> dict[str, list[HasAccountNameT]]:
    """Groups items by their account name.

    Args:
        items (Iterable[HasAccountNameT]): An iterable of items that have
            an account_name attribute.

    Returns:
        AccountNameToItemsT: A dictionary where keys are account names
            and values are lists of items with that account name.
    """
    account_name_to_items: dict[str, list[HasAccountNameT]] = defaultdict(list)
    for item in items:
        account_name_to_items[item.account_name].append(item)
    return dict(account_name_to_items)

def prepare_events(
        *,
        account_name_to_unit: Mapping[str, Unit],
        canceled_orders: Iterable[DetailedOrder],
        country_code: CountryCode,
) -> list[Event]:
    account_name_to_orders = group_by_account_name(canceled_orders)
    events: list[Event] = []

    for account_name, grouped_orders in account_name_to_orders.items():

        try:
            unit = account_name_to_unit[account_name]
        except KeyError:
            logger.error('No unit found', account_name=account_name)
            continue

        orders = [
            EventPayloadOrder(
                id=order.id,
                number=order.number,
                price=order.payment.price,
                sales_channel=order.sales_channel,
                is_refund_receipt_printed=order.is_refund_receipt_printed,
            )
            for order in grouped_orders
        ]

        event_payload = EventPayload(
            orders=orders,
            unit_name=unit.name,
            country_code=country_code,
        )
        event = Event(unit_ids=[unit.id], payload=event_payload)
        events.append(event)

    return events