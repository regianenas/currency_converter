from django.db import models
from django.utils import timezone


class Product(models.Model):
    """
    The Product object contains the name of a registered product.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Prices(models.Model):
    """
    The Prices object contains all prices in each currency for a registered product.
    """

    class Meta:
        unique_together = [("product", "slug_code")]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    slug_code = models.SlugField()
    currency_country = models.CharField(max_length=255)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug_code
