from django.urls import path
from converter import views

app_name = "converter"
urlpatterns = [
    path("", views.get_create_product, name="products"),
    path("<str:name>", views.get_update_or_delete_prices_per_product, name="products"),
]
