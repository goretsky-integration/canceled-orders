from collections import defaultdict
from collections.abc import Iterable
from typing import Protocol, TypeVar

import structlog.stdlib

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
