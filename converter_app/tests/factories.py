from decimal import Decimal
import factory

from django.utils import timezone
from datetime import datetime
from faker import Faker
from converter.models import Product, Prices


fake = Faker()
date = datetime(2022, 8, 1, 9, 30, 23, tzinfo=timezone.utc)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("product_name")
    description = fake.text()
    create_date = date
    update_date = date


class PricesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Prices

    # product = ProductFactory.build()
    product = factory.SubFactory(ProductFactory)
    slug_code = fake.slug()
    currency_country = factory.Faker("country")
    value = Decimal("529.29")
    create_date = date
    update_date = date
