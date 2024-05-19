from enum import StrEnum, auto

__all__ = ('CountryCode', 'SalesChannel')


class CountryCode(StrEnum):
    RU = auto()


class SalesChannel(StrEnum):
    DELIVERY = auto()
    DINE_IN = auto()
