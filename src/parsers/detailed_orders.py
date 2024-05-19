import json

import httpx
from pydantic import ValidationError

from models import DetailedOrder

__all__ = ('parse_detailed_order_response',)


def parse_detailed_order_response(
        response: httpx.Response,
        account_name: str,
) -> DetailedOrder:
    try:
        response_data = response.json()
        response_data |= {'account_name': account_name}
        return DetailedOrder.model_validate(response_data)
    except (json.JSONDecodeError, ValidationError) as error:
        raise
