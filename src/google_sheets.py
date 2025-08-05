import time
from collections.abc import Iterable

import gspread
from gspread.utils import ValueInputOption

from models import DetailedOrder, Unit

UNIT_NAME_TO_ABBREVIATION = {
    'Подольск-3': 'П-3',
    'Подольск-2': 'П-2',
    'Подольск-1': 'П-1',
    'Подольск-4': 'П-4',
    'Москва 4-16': '4-16',
    'Москва 4-9': '4-9',
    'Москва 4-8': '4-8',
    'Москва 4-19': '4-19',
    'Москва 4-18': '4-18',
    'Москва 4-17': '4-17',
    'Москва 4-15': '4-15',
    'Москва 4-14': '4-14',
    'Москва 4-13': '4-13',
    'Москва 4-12': '4-12',
    'Москва 4-11': '4-11',
    'Москва 4-7': '4-7',
    'Москва 4-6': '4-6',
    'Москва 4-5': '4-5',
    'Москва 4-4': '4-4',
    'Москва 4-3': '4-3',
    'Москва 4-10': '4-10',
    'Москва 4-2': '4-2',
    'Москва 4-1': '4-1',
    'Калуга-1': 'К-1',
    'Калуга-2': 'К-2',
    'Калуга-3': 'К-3',
    'Смоленск-1': 'С-1',
    'Смоленск-2': 'С-2',
    'Смоленск-3': 'С-3',
    'Смоленск-4': 'С-4',
    'Вязьма-1': 'В-1',
    'Обнинск-1': 'О-1',
}


class GoogleSheetsGateway:

    def __init__(
        self,
        spreadsheet: gspread.Spreadsheet,
        units: Iterable[Unit],
    ):
        self.__spreadsheet = spreadsheet
        self.__title_to_worksheet: dict[str, gspread.Worksheet] = {}
        self.__units = units
        self.__account_name_to_unit_name = {
            unit.account_name: unit.name for unit in units
        }

    def delete_sheets(self) -> None:
        for unit in self.__units:
            abbreviated_title = UNIT_NAME_TO_ABBREVIATION.get(
                unit.name, unit.name,
            )
            if abbreviated_title in self.__title_to_worksheet:
                worksheet = self.__title_to_worksheet[abbreviated_title]
                self.__spreadsheet.del_worksheet(worksheet)
                del self.__title_to_worksheet[abbreviated_title]


    def init_sheets(self):
        worksheets = self.__spreadsheet.worksheets()
        title_to_worksheet = {ws.title: ws for ws in worksheets}

        unit_names = {unit.name for unit in self.__units}
        for unit_name in unit_names:
            abbreviated_title = UNIT_NAME_TO_ABBREVIATION.get(
                unit_name, unit_name,
            )

            if abbreviated_title not in title_to_worksheet:
                worksheet = self.__spreadsheet.add_worksheet(
                    title=abbreviated_title, rows=20, cols=10,
                )
                worksheet.append_row(
                    [
                        'Дата заказа',
                        'Тип заказа',
                        'Номер заказа',
                        'Сумма заказа',
                        'Номер телефона',
                        'Дата дозвона',
                        'Статус дозвона',
                        'Комментарий',
                    ],
                )
                title_to_worksheet[abbreviated_title] = worksheet

        self.__title_to_worksheet = title_to_worksheet

    def append_order(self, order: DetailedOrder) -> None:
        try:
            unit_name = self.__account_name_to_unit_name[order.account_name]
        except KeyError:
            return

        abbreviation = UNIT_NAME_TO_ABBREVIATION.get(unit_name, unit_name)

        if abbreviation not in self.__title_to_worksheet:
            return

        order_url = f'=HYPERLINK("https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/Orders#/order/{order.id.hex.upper()}"; "{order.number}")'
        worksheet = self.__title_to_worksheet[abbreviation]
        worksheet.append_row(
            [
                f'{order.created_at:%d.%m.%Y %H:%M:%S}',
                'Доставка' if order.courier_needed else 'Ресторан',
                order_url,
                order.payment.price,
                order.client.phone,
            ],
            value_input_option=ValueInputOption.user_entered,
        )
        time.sleep(2.5)
