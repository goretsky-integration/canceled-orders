import factory

from factories.partial_orders import PartialOrderFactory
from models import (
    DetailedOrder,
    DetailedOrderDelivery,
    DetailedOrderHistoryItem,
    DetailedOrderPayment,
)

__all__ = (
    'DetailedOrderFactory',
    'DetailedOrderDeliveryFactory',
    'DetailedOrderPaymentFactory',
    'DetailedOrderHistoryItemFactory',
)


class DetailedOrderDeliveryFactory(factory.Factory):
    class Meta:
        model = DetailedOrderDelivery

    courier = factory.Faker('word')


class DetailedOrderPaymentFactory(factory.Factory):
    class Meta:
        model = DetailedOrderPayment

    price = factory.Faker('random_int')


class DetailedOrderHistoryItemFactory(factory.Factory):
    class Meta:
        model = DetailedOrderHistoryItem

    date = factory.Faker('date_time')
    description = factory.Faker('sentence')
    user_name = factory.Faker('name')


class DetailedOrderFactory(PartialOrderFactory):
    class Meta:
        model = DetailedOrder

    id = factory.Faker('uuid4')
    account_name = factory.Faker('name')
    courier_needed = factory.Faker('boolean')
    history = factory.List(
        [factory.SubFactory(DetailedOrderHistoryItemFactory)],
    )
    number = factory.Sequence(lambda n: f'{n + 1}-0')
    payment = factory.SubFactory(DetailedOrderPaymentFactory)
    delivery = factory.SubFactory(DetailedOrderDeliveryFactory)
