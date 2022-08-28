import pytest

from pytest_factoryboy import register
from tests.factories import ProductFactory, PricesFactory

register(ProductFactory)
register(PricesFactory)




