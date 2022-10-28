from typing import Final
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from .models import Payment
from .serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentSuccessSerializer,
    PaymentCancelSerializer,
)
from products.permissions import IsAdminOrReadOnly


class PaymentListView(APIView):

    permission_classes: Final = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        """
        결제 내역 목록
        GET /api/v1/payments/
        """

        payments: Final = Payment.objects.all()
        serializer: Final = PaymentListSerializer(payments, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        결제 내역 생성
        POST /api/v1/payments/
        """

        serializer: PaymentSerializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment: Payment = serializer.save()
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PaymentView(APIView):

    permission_classes: Final = [IsAdminOrReadOnly]

    def get_object(self, pk: int) -> Payment:
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise NotFound

    def get(self, request: Request, pk: int) -> Response:
        """
        결제 내역 상세
        GET /api/v1/payments/{pk}/
        """

        payment: Final = self.get_object(pk)
        serializer: Final = PaymentSerializer(payment)
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        """
        결제 내역 수정
        PATCH /api/v1/payments/{pk}/
        """

        payment: Payment = self.get_object(pk)
        match request.data:
            case {"successed_at": successed_at} if successed_at is not None:
                serializer: PaymentSuccessSerializer = PaymentSuccessSerializer(
                    payment, data=request.data, partial=True
                )
            case {"canceled_at": canceled_at} if canceled_at is not None:
                serializer: PaymentCancelSerializer = PaymentCancelSerializer(
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

    def delete(self, request: Request, pk: int) -> Response:
        """
        결제 내역 삭제
        DELETE /api/v1/payments/{pk}/
        """

        payment: Final = self.get_object(pk)
        payment.delete()
        return Response(status=HTTP_204_NO_CONTENT)
