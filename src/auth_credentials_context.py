from collections.abc import Iterable

import structlog.stdlib

from connections import AuthCredentialsStorageConnection
from connections.helpers import retry_on_failure
from models import AccountCookies
from parsers import parse_account_cookies_response

__all__ = ('AuthCredentialsContext',)

from tasks_executor import execute_batched_tasks

logger = structlog.stdlib.get_logger('parser')


class AuthCredentialsContext:

    def __init__(
            self,
            auth_credentials_connection: AuthCredentialsStorageConnection,
    ):
        self.__auth_credentials_connection = auth_credentials_connection

    @retry_on_failure(attempts=5)
    async def get_account_cookies(
            self,
            account_name: str,
    ) -> AccountCookies:
        response = (
            await self.__auth_credentials_connection.get_account_cookies(
                account_name=account_name,
            )
        )
        return parse_account_cookies_response(
            response=response,
            account_name=account_name,
        )

    async def get_accounts_cookies_batch(
            self,
            account_names: Iterable[str],
    ) -> list[AccountCookies]:
        tasks = [
            self.get_account_cookies(account_name)
            for account_name in account_names
        ]
        accounts_cookies = await execute_batched_tasks(tasks)

        result: list[AccountCookies] = []
        for account_cookies in accounts_cookies:
            if isinstance(account_cookies, Exception):
                logger.exception('Could not get auth credentials')
            else:
                result.append(account_cookies)

        return result
