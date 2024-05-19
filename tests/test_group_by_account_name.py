from dataclasses import dataclass

import pytest

from mappers import group_by_account_name


@dataclass(frozen=True, slots=True)
class Item:
    account_name: str


def test_group_by_account_name():
    items = [
        Item(account_name='Alice'),
        Item(account_name='Bob'),
        Item(account_name='Alice'),
        Item(account_name='Charlie'),
        Item(account_name='Bob'),
    ]

    result = group_by_account_name(items)

    expected = {
        'Alice': [
            Item(account_name='Alice'),
            Item(account_name='Alice'),
        ],
        'Bob': [
            Item(account_name='Bob'),
            Item(account_name='Bob'),
        ],
        'Charlie': [
            Item(account_name='Charlie'),
        ],
    }

    assert result == expected


def test_empty_list():
    items = []
    result = group_by_account_name(items)
    assert result == {}


def test_single_item():
    items = [Item(account_name='Alice')]
    result = group_by_account_name(items)
    expected = {'Alice': [Item(account_name='Alice')]}
    assert result == expected


def test_multiple_items_same_account_name():
    items = [
        Item(account_name='Alice'),
        Item(account_name='Alice'),
        Item(account_name='Alice')
    ]
    result = group_by_account_name(items)
    expected = {
        'Alice': [
            Item(account_name='Alice'),
            Item(account_name='Alice'),
            Item(account_name='Alice'),
        ]
    }
    assert result == expected


def test_no_account_name_attribute():
    class ItemWithoutAccountName:
        pass

    items = [ItemWithoutAccountName()]

    with pytest.raises(AttributeError):
        group_by_account_name(items)


if __name__ == "__main__":
    pytest.main()
