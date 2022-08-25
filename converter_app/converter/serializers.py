from converter.models import Product, Prices
from rest_framework import serializers


class PricesSerializer(serializers.ModelSerializer):
    """
    Responsible for converting a Price object into datatypes that can
    be rendered into JSON or XML.
    """

    class Meta:
        model = Prices
        fields = ["slug_code", "value", "currency_country"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Responsible for converting a Product object into datatypes that can
    be rendered into JSON or XML.
    """

    prices = PricesSerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "prices"]

    def create(self, validated_data: dict) -> Product:
        """
        Create Product with data from request.
        """
        prices_data = validated_data.pop("prices")
        product = Product.objects.create(**validated_data)
        for price_data in prices_data:
            Prices.objects.create(product=product, **price_data)
        return product

    def update(self, obj: Product, validated_data: dict) -> Product:
        """
        Update Product with data from request.
        """
        prices_data = validated_data.pop("prices")
        Product.objects.filter(name=validated_data["name"]).update(**validated_data)
        Prices.objects.filter(product=obj).delete()
        for price_data in prices_data:
            Prices.objects.create(product=obj, **price_data)
        return obj
