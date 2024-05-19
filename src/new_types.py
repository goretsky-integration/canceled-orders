from typing import NewType

import httpx

__all__ = (
    'AuthCredentialsStorageHttpClient',
    'DodoIsHttpClient',
)

AuthCredentialsStorageHttpClient = NewType(
    'AuthCredentialsStorageHttpClient',
    httpx.AsyncClient,
)
DodoIsHttpClient = NewType('DodoIsHttpClient', httpx.AsyncClient)
