from typing import Dict, Any, Optional, Final
from rest_framework import serializers
from .models import Payment

ATTRS_TYPE = Dict[str, Optional[str | Any]]
COMMON_FIELDS: Final = (
    "id",
    "product",
    "user",
    "price",
    "delivery_fee",
    "amount",
    "payment_method",
    "successed_at",
    "canceled_at",
    "created_at",
    "updated_at",
)  # 공통 필드 -> 추후 필요에 따라 분리


class PaymentSerializer(serializers.ModelSerializer):
    """
    결제내역 Serializer
    """

    class Meta:
        model: Final = Payment
        fields: Final = COMMON_FIELDS


class PaymentUpdateCommonSerializer(serializers.ModelSerializer):
    """
    결제내역 Update를 위한 추상적 Serializer
    """

    ESSENTIAL_FIELDS: str = ""
    COMPARE_FIELDS: str = ""

    def validate(self, attrs: ATTRS_TYPE) -> ATTRS_TYPE:
        # 필수 필드 검사
        if attrs.get(self.ESSENTIAL_FIELDS, None) is None:
            raise serializers.ValidationError(f"{self.ESSENTIAL_FIELDS}가 없습니다.")
        if attrs.get(self.COMPARE_FIELDS, None) is None:
            raise serializers.ValidationError(f"{self.COMPARE_FIELDS}가 없습니다.")
        if attrs.get(self.COMPARE_FIELDS) <= attrs.get(self.ESSENTIAL_FIELDS):
            return attrs
        raise serializers.ValidationError(
            f"{self.ESSENTIAL_FIELDS}가 {self.COMPARE_FIELDS}보다 이전입니다."
        )


class PaymentSuccessSerializer(PaymentUpdateCommonSerializer):
    """
    결제 성공 Serializer
    """

    ESSENTIAL_FIELDS: Final = "successed_at"
    COMPARE_FIELDS: Final = "created_at"

    class Meta:
        model: Final = Payment
        fields: Final = ("successed_at",)


class PaymentCancelSerializer(PaymentUpdateCommonSerializer):
    """
    결제 취소 Serializer
    """

    ESSENTIAL_FIELDS: Final = "canceled_at"
    COMPARE_FIELDS: Final = "successed_at"

    class Meta:
        model: Final = Payment
        fields: Final = ("canceled_at",)
