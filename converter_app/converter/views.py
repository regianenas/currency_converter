from converter.models import Product
from converter.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import logging

logger = logging.getLogger(__name__)


@api_view(["GET", "PUT", "DELETE"])
def get_update_or_delete_prices_per_product(
    request: Request,
    name: str,
) -> Response:
    """
    API endpoint that allows product prices to be viewed, update or delete.
    """
    try:
        product = Product.objects.get(name=name)
    except Product.DoesNotExist:
        logger.error(f"{name} is not registered in database.")
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Product {name} was updated:{request.data}")
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        logger.error(f"Error when try to register product {serializer.errors}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        product.delete()
        logger.info(f"Product {name} was deleted from database.")
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "GET"])
def get_create_product(request: Request) -> Response:
    """
    API endpoint that allows to get or create a product and prices.
    """
    if request.method == "GET":
        paginator = PageNumberPagination()
        paginator.page_size = 10
        products = Product.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"New product was registered {request.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Error when try to register product {serializer.errors}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
