from enum import IntEnum, StrEnum, auto

__all__ = ('CountryCode', 'SalesChannel', 'OrderState')


class CountryCode(StrEnum):
    RU = auto()


class SalesChannel(IntEnum):
    DINE_IN = 3
    TAKEAWAY = 2
    DELIVERY = 1


class OrderState(IntEnum):
    ACCEPTED = 1
    IN_PROGRESS = 2
    PACKED = 3
    DELIVERY = 4
    LATE = 11
    CANCELED = 12
