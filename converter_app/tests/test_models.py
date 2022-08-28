from datetime import datetime

import pytest

from collections import defaultdict
from converter.models import Product, Prices
from decimal import Decimal
from django.db import IntegrityError
from django.utils import timezone


@pytest.fixture
def current_date():
    return datetime(2022, 8, 1, 9, 30, 23, tzinfo=timezone.utc)


@pytest.fixture
def product_payload():
    return {
        "name": "Tenis nike'",
        "description": "Tenis feminino preto e rosa",
    }


@pytest.fixture
def prices_payload():
    return [
        {"slug_code": "BRL", "value": "529.29", "currency_country": "Brazil"},
        {"slug_code": "USD", "value": "98.23", "currency_country": "United States"},
        {"slug_code": "EUR", "value": "83.26", "currency_country": "Countries in Europe"},
        {"slug_code": "INR", "value": "7318.93", "currency_country": "India"},
    ]


@pytest.fixture
def repeated_prices_payload():
    return [
        {"slug_code": "BRL", "value": "529.29", "currency_country": "Brazil"},
        {"slug_code": "USD", "value": "98.23", "currency_country": "United States"},
        {"slug_code": "USD", "value": "88.23", "currency_country": "United States"},
        {"slug_code": "EUR", "value": "83.26", "currency_country": "Countries in Europe"},
        {"slug_code": "INR", "value": "7318.93", "currency_country": "India"},
    ]


@pytest.mark.django_db
@pytest.mark.freeze_time("2022-08-01 9:30:23")
def test_create_product(product_payload, product_factory, current_date):
    """
    Create a Product instance from a payload.
    """
    product = product_factory.build(**product_payload)
    assert product.name == product_payload["name"]
    assert product.description == product_payload["description"]
    assert product.create_date == current_date
    assert product.update_date == current_date


@pytest.mark.django_db
def test_not_create_product_already_exist(product_payload, product_factory):
    """
    Raise an Integrity error when try to create a Product that already exist.
    """
    product_factory.create(**product_payload)
    with pytest.raises(IntegrityError):
        Product.objects.create(**product_payload)


@pytest.mark.django_db
@pytest.mark.freeze_time("2022-08-01 9:30:23")
def test_create_prices(
    prices_payload, product_payload, product_factory, prices_factory, current_date
):
    """
    Create a Prices instance from a payload.
    """
    prices_json_map = defaultdict(list)
    for price in prices_payload:
        prices_json_map["slug_code"].append(price["slug_code"])
        prices_json_map["currency_country"].append(price["currency_country"])
        prices_json_map["value"].append(Decimal(price["value"]))

    product = product_factory.create(**product_payload)
    for price in prices_payload:
        prices_factory.create(product=product, **price)

    for price in product.prices.all():
        assert price.slug_code in prices_json_map["slug_code"]
        assert price.currency_country in prices_json_map["currency_country"]
        assert price.value in prices_json_map["value"]
        assert price.create_date == current_date
        assert price.update_date == current_date
