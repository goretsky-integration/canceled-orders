from datetime import date

import pytest

from connections.dodo_is import build_partial_orders_request_payload
from enums import OrderState, SalesChannel


def test_default_parameters():
    payload = build_partial_orders_request_payload(date=date(2023, 5, 19))
    assert payload == {
        'date': '2023-05-19',
        'perPage': 100,
        'page': 1,
    }


def test_specific_date_page_per_page():
    payload = build_partial_orders_request_payload(date=date(2023, 5, 19),
                                                   page=2, per_page=50)
    assert payload == {
        'date': '2023-05-19',
        'perPage': 50,
        'page': 2,
    }


def test_with_sales_channel():
    payload = build_partial_orders_request_payload(
        date=date(2023, 5, 19),
        sales_channel=SalesChannel.DINE_IN,
    )
    assert payload == {
        'date': '2023-05-19',
        'perPage': 100,
        'page': 1,
        'orderType': SalesChannel.DINE_IN,
    }


def test_with_order_state():
    payload = build_partial_orders_request_payload(
        date=date(2023, 5, 19),
        order_state=OrderState.DELIVERY,
    )
    assert payload == {
        'date': '2023-05-19',
        'perPage': 100,
        'page': 1,
        'state': OrderState.DELIVERY,
    }


def test_with_all_parameters():
    payload = build_partial_orders_request_payload(
        date=date(2023, 5, 19),
        sales_channel=SalesChannel.DINE_IN,
        order_state=OrderState.LATE,
        page=3,
        per_page=25
    )
    assert payload == {
        'date': '2023-05-19',
        'perPage': 25,
        'page': 3,
        'orderType': SalesChannel.DINE_IN,
        'state': OrderState.LATE,
    }


def test_with_sales_channel_and_order_state():
    payload = build_partial_orders_request_payload(
        date=date(2023, 5, 19),
        sales_channel=SalesChannel.DELIVERY,
        order_state=OrderState.IN_PROGRESS
    )
    assert payload == {
        'date': '2023-05-19',
        'perPage': 100,
        'page': 1,
        'orderType': SalesChannel.DELIVERY,
        'state': OrderState.IN_PROGRESS,
    }


if __name__ == "__main__":
    pytest.main()
