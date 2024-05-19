import asyncio
import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

import structlog.stdlib

__all__ = ('retry_on_failure',)

logger = structlog.stdlib.get_logger('app')

T = TypeVar("T")
P = ParamSpec('P')


def retry_on_failure(attempts: int) -> Callable[[Callable[P, T]], Callable[P, T]]:
    if attempts < 1:
        raise ValueError("Attempts must be greater than 0")

    def decorator(func: Callable[P, T]) -> Callable[P, T]:

        if not asyncio.iscoroutinefunction(func):
            raise ValueError('Function must be async')

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for _ in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as error:
                    logger.warning(
                        f'Failed to execute "{func.__name__}"'
                        f' due to error: {error}',
                    )
            raise Exception(
                f'Failed to execute "{func.__name__}"'
                f' after {attempts} attempts'
            )

        return wrapper

    return decorator
