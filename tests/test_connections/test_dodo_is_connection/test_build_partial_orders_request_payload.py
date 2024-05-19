from datetime import date

import pytest

from connections.dodo_is import (
    build_partial_orders_request_payload,
    CANCELED_ORDER_STATE_ID,
)


def test_default_parameters():
    payload = build_partial_orders_request_payload(
        date=date(2023, 5, 19)
    )
    assert payload == {
        'date': '2023-05-19',
        'perPage': 100,
        'page': 1,
        'state': CANCELED_ORDER_STATE_ID,
    }


def test_specific_date_page_per_page():
    payload = build_partial_orders_request_payload(
        date=date(2023, 5, 19),
        page=2,
        per_page=50,
    )
    assert payload == {
        'date': '2023-05-19',
        'perPage': 50,
        'page': 2,
        'state': CANCELED_ORDER_STATE_ID,
    }


if __name__ == "__main__":
    pytest.main()
