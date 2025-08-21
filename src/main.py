import asyncio
import datetime

import gspread
from fast_depends import Depends, inject

from auth_credentials_context import AuthCredentialsContext
from config import Config, get_config, load_google_sheets_credentials
from dependencies import (
    get_auth_credentials_context,
    get_dodo_is_context,
)
from dodo_is_context import DodoIsContext
from enums import CountryCode
from filters import filter_valid_canceled_orders
from google_sheets import GoogleSheetsGateway
from mappers import prepare_events
from message_queue import publish_events
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
    client = gspread.service_account_from_dict(load_google_sheets_credentials())
    spreadsheet = client.open_by_key(config.spreadsheet_id)

    load_google_sheets_credentials()
    account_names = {unit.account_name for unit in units}
    accounts_cookies = (
        await auth_credentials_context.get_accounts_cookies_batch(
            account_names=account_names,
        )
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
        country_code=CountryCode.RU,
    )

    google_sheets_gateway = GoogleSheetsGateway(
        spreadsheet=spreadsheet, units=units
    )
    google_sheets_gateway.init_sheets()
    total = len(filtered_canceled_orders)
    for i, order in enumerate(filtered_canceled_orders, start=1):
        google_sheets_gateway.append_order(order)
        print(f"Appended order {i}/{total}")


if __name__ == "__main__":
    asyncio.run(main())
