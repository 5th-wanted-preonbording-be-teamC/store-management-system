from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Product
from .serializers import ProductListSerializer


class Products(APIView):
    def get(self, request):
        """
        상품 목록
        GET /api/v1/products/
        """
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request):
        pass


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
