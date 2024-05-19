import datetime
from typing import Final
from uuid import UUID

import httpx
import structlog.stdlib
from structlog.contextvars import bound_contextvars

from new_types import DodoIsHttpClient

__all__ = (
    'DodoIsConnection',
    'build_partial_orders_request_payload',
    'CANCELED_ORDER_STATE_ID',
)

logger = structlog.stdlib.get_logger('Dodo IS Connection')

CANCELED_ORDER_STATE_ID: Final[int] = 12


def build_partial_orders_request_payload(
        *,
        date: datetime.date,
        page: int = 1,
        per_page: int = 100,
) -> dict[str, str | int]:
    query_params = {
        'date': f'{date:%Y-%m-%d}',
        'perPage': per_page,
        'page': page,
        'state': CANCELED_ORDER_STATE_ID,
    }
    return query_params


class DodoIsConnection:

    def __init__(self, http_client: DodoIsHttpClient):
        self.__http_client = http_client

    async def get_partial_orders(
            self,
            *,
            cookies: dict[str, str],
            date: datetime.date,
            page: int = 1,
            per_page: int = 100,
    ) -> httpx.Response:
        """
        Retrieve partial orders from Dodo IS.

        Keyword Args:
            cookies: Cookies to be sent with the request.
            date: Date of orders to retrieve.
            page: Page number.
            per_page: Number of orders per page.

        Returns:
            httpx.Response object.
        """
        url = '/api/orders'
        query_params = build_partial_orders_request_payload(
            date=date,
            page=page,
            per_page=per_page,
        )
        with bound_contextvars(query_params=query_params):
            logger.debug('Retrieving partial orders')
            response = await self.__http_client.get(
                url=url,
                params=query_params,
                cookies=cookies,
            )
            logger.debug(
                'Partial orders retrieved',
                status_code=response.status_code,
            )
        return response

    async def get_detailed_order(
            self,
            *,
            cookies: dict[str, str],
            order_id: UUID,
    ) -> httpx.Response:
        url = f'/api/orders/{order_id.hex.upper()}'
        response = await self.__http_client.get(url=url, cookies=cookies)
        return response
