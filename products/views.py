from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer
from .permissions import IsAdminOrReadOnly


class Products(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """
        상품 목록
        GET /api/v1/products/
        """
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request):
        """
        상품 생성
        POST /api/v1/products/
        """
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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
