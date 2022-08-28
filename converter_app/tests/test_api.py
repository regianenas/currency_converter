import pytest
import json
from rest_framework.test import APIClient
from rest_framework import status
from converter.models import Product

EMPTY = b""
SLUG_CODES = ["BRL", "USD"]
PRICES_VALUE = [250.85, 35.45]
COUNTRY = ["Brazil", "United States"]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def payload():
    return {
        "name": "Tenis puma",
        "prices": [
            {"slug_code": "BRL", "value": "250.85", "currency_country": "Brazil"},
            {"slug_code": "USD", "value": "35.45", "currency_country": "United States"},
        ],
    }


@pytest.fixture()
def updated_payload():
    return {
        "name": "Tenis puma",
        "prices": [
            {"slug_code": "BRL", "value": "329.25", "currency_country": "Brazil"},
            {"slug_code": "USD", "value": "35.45", "currency_country": "United States"},
        ],
    }


@pytest.fixture()
def updated_with_remove_price_payload():
    return {
        "name": "Tenis puma",
        "prices": [{"slug_code": "BRL", "value": "329.25", "currency_country": "Brazil"}],
    }


@pytest.fixture()
def all_product_payload():
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "name": "Tenis puma",
                "prices": [
                    {"currency_country": "Brazil", "slug_code": "BRL", "value": "250.85"},
                    {"currency_country": "United States", "slug_code": "USD", "value": "35.45"},
                ],
            }
        ],
    }


@pytest.mark.django_db
def test_create_product(api_client, payload):
    """Call api to create  a product successfully."""
    response = api_client.post("/products/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert json.loads(response.content) == payload

    product = Product.objects.get(name=payload["name"])
    product.name = payload["name"]
    for i, price in enumerate(product.prices.all()):
        price.currency_country = COUNTRY[i]
        price.slug_code == SLUG_CODES[i]
        price.value == PRICES_VALUE[i]


@pytest.mark.django_db
def test_create_product_fails_same_name(api_client, payload):
    """Call api to create a product that exist at database already."""
    api_client.post("/products/", payload, format="json")
    response = api_client.post("/products/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_product(api_client, payload):
    """Call api to delete a product successfully."""
    api_client.post("/products/", payload, format="json")
    # Before delete
    product = Product.objects.get(name=payload["name"])
    product.name = payload["name"]
    for i, price in enumerate(product.prices.all()):
        price.currency_country = COUNTRY[i]
        price.slug_code == SLUG_CODES[i]
        price.value == PRICES_VALUE[i]

    response = api_client.delete(f'/products/{payload["name"]}', format="json")
    # After delete
    product = Product.objects.filter(name=payload["name"]).last()

    assert product is None
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == EMPTY


@pytest.mark.django_db
def test_get_all_product(api_client, payload, all_product_payload):
    """Call api to get all product in database successfully."""
    api_client.post("/products/", payload, format="json")
    response = api_client.get("/products/", format="json")

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == all_product_payload


@pytest.mark.django_db
def test_get_one_product(api_client, payload):
    """Call api to get a specific product in database successfully."""
    api_client.post("/products/", payload, format="json")
    response = api_client.get(f'/products/{payload["name"]}', format="json")

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == payload


@pytest.mark.django_db
def test_get_non_existent_product(api_client):
    """Call api to get a non existent product in database."""
    response = api_client.get("/products/Tenis nike", format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_product(api_client, payload, updated_payload):
    """Call api to update the Brazilian price in the product successfully."""
    api_client.post("/products/", payload, format="json")
    # Before update
    prices_before = Product.objects.get(name=payload["name"]).prices.all()
    for i, price in enumerate(prices_before):
        price.slug_code == SLUG_CODES[i]
        price.value == PRICES_VALUE[i]

    response = api_client.put(
        f'/products/{updated_payload["name"]}', updated_payload, format="json"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == EMPTY

    # After update
    prices_after_value = [329.25, 35.45]
    prices_after = Product.objects.get(name=updated_payload["name"]).prices.all()
    for i, price in enumerate(prices_after):
        price.slug_code == SLUG_CODES[i]
        price.value == prices_after_value[i]


@pytest.mark.django_db
def test_remove_one_price_product(
    api_client, payload, updated_with_remove_price_payload
):
    """Call api to update removing the American price in the product successfully."""
    name = updated_with_remove_price_payload["name"]
    api_client.post("/products/", payload, format="json")
    # Before update
    prices_before = Product.objects.get(name=payload["name"]).prices.all()
    for i, price in enumerate(prices_before):
        price.slug_code == SLUG_CODES[i]
        price.value == PRICES_VALUE[i]

    response = api_client.put(
        f"/products/{name}", updated_with_remove_price_payload, format="json"
    )

    # After update
    price_value = [329.25]
    slug_code = ["BRL"]
    prices_after = Product.objects.get(name=name).prices.all()
    for i, price in enumerate(prices_after):
        price.slug_code == slug_code[i]
        price.value == price_value[i]

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == EMPTY
