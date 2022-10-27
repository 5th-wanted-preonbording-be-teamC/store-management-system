from rest_framework import serializers
from .models import Payment

common_fields = (
    "id",
    "product",
    "user",
    "price",
    "delivery_fee",
    "amount",
    "payment_method",
    "delivery_address",
    "successed_at",
    "canceled_at",
    "deliveried_at",
    "shiped_at",
    "created_at",
    "updated_at",
) # 공통 필드
indivisual_fields = tuple() # 개별 필드
list_fields = tuple() # 리스트 필드

class PaymentSerializer(serializers.ModelSerializer):
    """
    결제내역 Serializer
    """
    class Meta:
        model = Payment
        fields = common_fields + indivisual_fields


class PaymentListSerializer(serializers.ModelSerializer):
    """
    결제내역 List Serializer
    결제내역 Serializer와 동일하나, 추후 필요시 변경할 수 있도록 분리
    """
    class Meta:
        model = Payment
        fields = common_fields + list_fields
