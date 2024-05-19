import httpx
from fast_depends import Depends

from config import Config, get_config
from new_types import (
    AuthCredentialsStorageHttpClient,
    DodoIsHttpClient,
)

__all__ = (
    'get_auth_credentials_storage_http_client',
    'get_dodo_is_http_client',
)


async def get_auth_credentials_storage_http_client(
        config: Config = Depends(get_config),
) -> AuthCredentialsStorageHttpClient:
    async with httpx.AsyncClient(
            base_url=config.auth_credentials_storage.base_url,
            timeout=config.auth_credentials_storage.http_client_timeout,
    ) as http_client:
        yield AuthCredentialsStorageHttpClient(http_client)



async def get_dodo_is_http_client(
        config: Config = Depends(get_config),
) -> DodoIsHttpClient:
    base_url = f'https://shiftmanager.dodopizza.{config.dodo_is.country_code}/'
    headers = {'User-Agent': config.app_name}

    async with httpx.AsyncClient(
            headers=headers,
            base_url=base_url,
            timeout=config.dodo_is.http_client_timeout,
    ) as http_client:
        yield DodoIsHttpClient(http_client)
