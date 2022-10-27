from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.exceptions import ParseError, NotFound
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
                    # TODO: 결제 관련 & 결제 검증 로직 추가
                    # ...

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


class OrderView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise NotFound

    def patch(self, request, pk):
        """
        주문 내역 상태 변경
        PATCH /api/v1/orders/{id}/
        """

        order = self.get_object(pk)

        # 주문자가 상품을 배송 받은 경우
        if order.user == request.user:
            order.status = Order.OrderStatusChoices.ARRIVED
            order.save()
            return Response(status=HTTP_200_OK)

        # 주문자가 상품을 발송한 경우
        if request.user.is_staff:
            order.status = Order.OrderStatusChoices.SENT
            order.save()
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)
