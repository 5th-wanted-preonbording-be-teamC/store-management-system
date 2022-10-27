from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from .models import Payment
from .serializers import (
    PaymentListSerializer,
    PaymentSerializer,
    PaymentSuccessSerializer,
    PaymentCancelSerializer,
    PaymentShipSerializer,
    PaymentDeliverySerializer,
    PaymentDeliveryAddressSerializer,
)
from products.permissions import IsAdminOrReadOnly


class PaymentListView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """
        결제 내역 목록
        GET /api/v1/payments/
        """

        payments = Payment.objects.all()
        serializer = PaymentListSerializer(payments, many=True)

        return Response(serializer.data)

    def post(self, request):
        """
        결제 내역 생성
        POST /api/v1/payments/
        """

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PaymentView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        """
        결제 내역 상세
        GET /api/v1/payments/{pk}/
        """

        payment = self.get_object(pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        결제 내역 수정
        PATCH /api/v1/payments/{pk}/
        """

        payment = self.get_object(pk)
        match request.data:
            case {"successed_at": successed_at}:
                serializer = PaymentSuccessSerializer(
                    payment, data=request.data, partial=True
                )
            case {"canceled_at": canceled_at}:
                serializer = PaymentCancelSerializer(
                    payment, data=request.data, partial=True
                )
            case {"shiped_at": shiped_at}:
                serializer = PaymentShipSerializer(
                    payment, data=request.data, partial=True
                )
            case {"delivered_at": delivered_at}:
                serializer = PaymentDeliverySerializer(
                    payment, data=request.data, partial=True
                )
            case {"delivery_adress": delivery_adress}:
                serializer = PaymentDeliveryAddressSerializer(
                    payment, data=request.data, partial=True
                )
            case _:
                return Response(
                    {"message": "변경할 수 있는 데이터가 없습니다."}, status=HTTP_400_BAD_REQUEST
                )

        if serializer.is_valid():
            payment = serializer.save()
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        결제 내역 삭제
        DELETE /api/v1/payments/{pk}/
        """

        payment = self.get_object(pk)
        payment.delete()
        return Response(status=HTTP_204_NO_CONTENT)
