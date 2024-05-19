import datetime
from collections.abc import Iterable

import structlog.stdlib

from connections.dodo_is import DodoIsConnection
from connections.helpers import retry_on_failure
from models import AccountCookies, DetailedOrder, PartialOrder
from parsers import (
    parse_detailed_order_response,
    parse_partial_orders_response,
)
from tasks_executor import execute_batched_tasks

__all__ = ('DodoIsContext',)

logger = structlog.stdlib.get_logger('parser')


class DodoIsContext:

    def __init__(self, dodo_is_connection: DodoIsConnection):
        self.__dodo_is_connection = dodo_is_connection

    @retry_on_failure(attempts=5)
    async def get_partial_orders(
            self,
            *,
            date: datetime.date,
            cookies: dict[str, str],
            per_page: int = 100,
    ) -> list[PartialOrder]:
        page = 1

        partial_orders: list[PartialOrder] = []
        while True:
            partial_orders_response = await self.__dodo_is_connection.get_partial_orders(
                cookies=cookies,
                date=date,
                page=page,
                per_page=per_page,
            )
            parsed_partial_orders_response = parse_partial_orders_response(
                response=partial_orders_response,
            )
            partial_orders += parsed_partial_orders_response.items

            if parsed_partial_orders_response.pagination.next_page is None:
                break

            page += 1

        return partial_orders

    async def get_detailed_order(
            self,
            *,
            account_cookies: AccountCookies,
            partial_order: PartialOrder,
    ) -> DetailedOrder:
        response = await self.__dodo_is_connection.get_detailed_order(
            cookies=account_cookies.cookies,
            order_id=partial_order.id,
        )
        return parse_detailed_order_response(
            response=response,
            account_name=account_cookies.account_name,
        )

    async def get_detailed_orders_batch(
            self,
            *,
            account_cookies: AccountCookies,
            partial_orders: Iterable[PartialOrder],
    ) -> list[DetailedOrder]:
        tasks = []
        for partial_order in partial_orders:
            tasks.append(
                self.get_detailed_order(
                    account_cookies=account_cookies,
                    partial_order=partial_order,
                ),
            )

        partial_order_responses = await execute_batched_tasks(tasks)

        result: list[DetailedOrder] = []
        for partial_order_response in partial_order_responses:
            if isinstance(partial_order_response, Exception):
                logger.error(
                    'Could not retrieve detailed order of partial order',
                    partial_order_id=partial_order_response,
                    account_name=account_cookies.account_name,
                )
            else:
                result.append(partial_order_response)

        return result

    async def get_account_canceled_orders(
            self,
            *,
            date: datetime.date,
            account_cookies: AccountCookies,
    ) -> list[DetailedOrder]:
        partial_orders: list[PartialOrder] = await self.get_partial_orders(
            date=date,
            cookies=account_cookies.cookies,
        )
        return await self.get_detailed_orders_batch(
            account_cookies=account_cookies,
            partial_orders=partial_orders,
        )

    async def get_accounts_canceled_orders_batch(
            self,
            *,
            date: datetime.date,
            account_cookies: Iterable[AccountCookies],
    ) -> list[DetailedOrder]:
        tasks = []
        for account_cookies in account_cookies:
            tasks.append(
                self.get_account_canceled_orders(
                    date=date,
                    account_cookies=account_cookies,
                ),
            )

        accounts_canceled_orders = await execute_batched_tasks(tasks)

        result: list[DetailedOrder] = []
        for account_canceled_orders in accounts_canceled_orders:
            if isinstance(account_canceled_orders, Exception):
                logger.error(
                    'Could not retrieve canceled orders of account',
                    account_name=account_canceled_orders,
                )
            else:
                result += account_canceled_orders

        return result
