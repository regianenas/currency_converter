from converter.models import Product, Prices
from rest_framework import serializers


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ["slug_code", "value", "currency_country"]


class ProductSerializer(
    serializers.ModelSerializer,
):
    prices = PricesSerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "prices"]

    def create(self, validated_data):
        prices_data = validated_data.pop("prices")
        product = Product.objects.create(**validated_data)
        for price_data in prices_data:
            Prices.objects.create(product=product, **price_data)
        return product

    def update(self, obj, validated_data):
        prices_data = validated_data.pop("prices")
        Product.objects.filter(name=validated_data["name"]).update(**validated_data)
        Prices.objects.filter(product=obj).delete()
        for price_data in prices_data:
            Prices.objects.create(product=obj, **price_data)
        return obj
