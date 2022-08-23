from django.db import models


class Product(models.Model):
    """
    The Product object contains the name of a registered product.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Prices(models.Model):
    """
    The Prices object contains all prices in each currency for a registered product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    slug_code = models.SlugField()
    currency_country = models.CharField(max_length=255)
    value = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.slug_code

