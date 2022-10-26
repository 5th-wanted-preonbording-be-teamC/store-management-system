from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
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

    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        """
        상품 상세
        GET /api/v1/products/{pk}/
        """

        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        상품 수정
        PATCH /api/v1/products/{pk}/
        """

        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        상품 삭제
        DELETE /api/v1/products/{pk}/
        """

        product = self.get_object(pk)
        product.delete()
        return Response(status=HTTP_204_NO_CONTENT)
