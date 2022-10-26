from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Product


class Products(APIView):
    def get(self, request):
        pass

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
