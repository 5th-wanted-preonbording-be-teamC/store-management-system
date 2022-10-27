from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ParseError
from .models import Order
from products.models import Product
from .serializers import OrderSerializer
from .permissions import OrderPermission


class OrdersView(APIView):

    permission_classes = [OrderPermission]

    def get(self, request):
        """
        주문 내역 확인
        GET /api/v1/orders/
        """

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        상품 주문
        POST /api/v1/orders/
        """

        serializer = OrderSerializer(data=request.data)
        products = request.data.get("products")

        if not products:
            raise ParseError("products is required.")

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    order = serializer.save(
                        user=request.user,
                        status=Order.OrderStatusChoices.PAYED,
                    )

                    products = request.data.get("products")
                    for product_pk in products:
                        product = Product.objects.get(pk=product_pk)
                        order.products.add(product)

                    serializer = OrderSerializer(order)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("not valid product id.")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
