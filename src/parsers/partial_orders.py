import json

import httpx
from pydantic import ValidationError

from models import PartialOrdersResponse

__all__ = ('parse_partial_orders_response',)


def parse_partial_orders_response(
        response: httpx.Response,
) -> PartialOrdersResponse:
    try:
        response_data = response.json()
        partial_orders_response = PartialOrdersResponse.model_validate(
            response_data,
        )
    except (json.JSONDecodeError, ValidationError) as error:
        raise

    return partial_orders_response
