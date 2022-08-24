from typing import Union

from converter.models import Product
from converter.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


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
        # put a log here
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "GET"])
def get_create_product(request: Request) -> Union[Response, PageNumberPagination]:
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
