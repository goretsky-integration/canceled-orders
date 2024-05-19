import operator
from collections.abc import Callable, Iterable
from functools import partial
from typing import TypeVar

from enums import SalesChannel
from models import DetailedOrder

__all__ = (
    'is_valid_canceled_order',
    'is_canceled_by_employee',
    'is_courier_assigned',
    'is_order_sales_channel',
    'all_lazy',
    'any_lazy',
    'filter_valid_canceled_orders',
)

T = TypeVar('T')

is_canceled_by_employee: Callable[[DetailedOrder], bool] = (
    operator.attrgetter('is_canceled_by_employee')
)
is_courier_assigned: Callable[[DetailedOrder], bool] = (
    operator.attrgetter('delivery.is_courier_assigned')
)


def is_order_sales_channel(
        item: DetailedOrder,
        sales_channel: SalesChannel,
) -> bool:
    return item.sales_channel == sales_channel


def all_lazy(*funcs: Callable[[T], bool]) -> Callable[[T], bool]:
    def wrapper(item: T) -> bool:
        return all(func(item) for func in funcs)

    return wrapper


def any_lazy(*funcs: Callable[[T], bool]) -> Callable[[T], bool]:
    def wrapper(item: T) -> bool:
        return any(func(item) for func in funcs)

    return wrapper


is_valid_canceled_order: Callable[[DetailedOrder], bool] = any_lazy(
    all_lazy(
        is_canceled_by_employee,
        partial(is_order_sales_channel, sales_channel=SalesChannel.DINE_IN),
    ),
    all_lazy(
        is_courier_assigned,
        partial(is_order_sales_channel, sales_channel=SalesChannel.DELIVERY),
    ),
)


def filter_valid_canceled_orders(
        orders: Iterable[DetailedOrder],
) -> list[DetailedOrder]:
    return [order for order in orders if is_valid_canceled_order(order)]
