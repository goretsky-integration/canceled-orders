from fast_depends import Depends

from connections import AuthCredentialsStorageConnection
from connections.dodo_is import DodoIsConnection
from dependencies.http_clients import (
    get_auth_credentials_storage_http_client,
    get_dodo_is_http_client,
)
from new_types import (
    AuthCredentialsStorageHttpClient,
    DodoIsHttpClient,
)

__all__ = (
    'get_auth_credentials_storage_connection',
    'get_dodo_is_connection',
)


async def get_auth_credentials_storage_connection(
        http_client: AuthCredentialsStorageHttpClient = Depends(
            get_auth_credentials_storage_http_client,
            use_cache=False,
        ),
) -> AuthCredentialsStorageConnection:
    yield AuthCredentialsStorageConnection(http_client)


async def get_dodo_is_connection(
        http_client: DodoIsHttpClient = Depends(
            get_dodo_is_http_client,
            use_cache=False,
        ),
) -> DodoIsConnection:
    yield DodoIsConnection(http_client)
