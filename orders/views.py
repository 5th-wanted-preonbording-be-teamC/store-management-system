from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrdersView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        주문 내역 확인
        GET /api/v1/orders/
        """

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
