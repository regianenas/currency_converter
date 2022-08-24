from django.contrib import admin

from converter.models import Product, Prices


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    search_fields = ["name"]


@admin.register(Prices)
class PricesAdmin(admin.ModelAdmin):

    search_fields = ["slug", "value", "currency_country"]
