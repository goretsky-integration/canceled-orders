import asyncio
import datetime

from fast_depends import Depends, inject

import message_queue
from auth_credentials_context import AuthCredentialsContext
from config import Config, get_config
from dependencies import (
    get_auth_credentials_context,
    get_dodo_is_context,
)
from dodo_is_context import DodoIsContext
from filters import filter_valid_canceled_orders
from mappers import prepare_events
from models import Unit
from time_helpers import get_yesterday_this_moment
from units_context import load_units


@inject
async def main(
        units: list[Unit] = Depends(load_units),
        auth_credentials_context: AuthCredentialsContext = Depends(
            get_auth_credentials_context,
        ),
        dodo_is_context: DodoIsContext = Depends(get_dodo_is_context),
        yesterday: datetime.datetime = Depends(
            get_yesterday_this_moment,
            use_cache=False,
        ),
        config: Config = Depends(get_config),
):
    account_names = {unit.account_name for unit in units}
    accounts_cookies = await auth_credentials_context.get_accounts_cookies_batch(
        account_names=account_names,
    )
    canceled_orders = await dodo_is_context.get_accounts_canceled_orders_batch(
        account_cookies=accounts_cookies,
        date=yesterday,
    )

    filtered_canceled_orders = filter_valid_canceled_orders(canceled_orders)

    account_name_to_unit = {unit.account_name: unit for unit in units}

    events = prepare_events(
        account_name_to_unit=account_name_to_unit,
        canceled_orders=filtered_canceled_orders,
        country_code=config.dodo_is.country_code,
    )

    await message_queue.publish_events(
        message_queue_url=config.message_queue_url,
        events=events,
    )


if __name__ == '__main__':
    asyncio.run(main())
