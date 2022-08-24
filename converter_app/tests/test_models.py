from decimal import Decimal

import pytest
from converter.models import Product, Prices
from django.db import IntegrityError


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


@pytest.mark.django_db
def test_create_product(product_payload):
    """
    Create a Product instance from a payload.
    """
    product = Product.objects.create(**product_payload)
    assert product.name == product_payload["name"]
    assert product.description == product_payload["description"]


@pytest.mark.django_db
def test_not_create_product_already_exist(product_payload):
    """
    Raise an Integrity error when try to create a Product that already exist.
    """
    Product.objects.create(**product_payload)
    with pytest.raises(IntegrityError):
        Product.objects.create(**product_payload)


@pytest.mark.django_db
def test_create_prices(prices_payload, product_payload):
    """
    Create a Prices instance from a payload.
    """
    product = Product.objects.create(**product_payload)
    for price in prices_payload:
        Prices.objects.create(product=product, **price)

    for i, price in enumerate(product.prices.all()):
        assert price.slug_code == prices_payload[i]["slug_code"]
        assert price.value == Decimal(prices_payload[i]["value"])
        assert price.currency_country == prices_payload[i]["currency_country"]
