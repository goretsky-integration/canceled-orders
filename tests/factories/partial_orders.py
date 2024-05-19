import factory

from models import PartialOrder

__all__ = ('PartialOrderFactory',)


class PartialOrderFactory(factory.Factory):
    class Meta:
        model = PartialOrder

    id = factory.Faker('uuid4')
