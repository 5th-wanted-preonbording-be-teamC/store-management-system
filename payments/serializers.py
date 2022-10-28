from typing import Dict, Any, Optional, Final
from rest_framework import serializers
from .models import Payment

AttrsType = Dict[str, Optional[str | Any]]
common_fields: Final = (
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
)  # 공통 필드
indivisual_fields: Final = tuple()  # 개별 필드
list_fields: Final = tuple()  # 리스트 필드


class PaymentSerializer(serializers.ModelSerializer):
    """
    결제내역 Serializer
    """

    class Meta:
        model: Final = Payment
        fields: Final = common_fields + indivisual_fields


class PaymentListSerializer(serializers.ModelSerializer):
    """
    결제내역 List Serializer
    결제내역 Serializer와 동일하나, 추후 필요시 변경할 수 있도록 분리
    """

    class Meta:
        model: Final = Payment
        fields: Final = common_fields + list_fields


class PaymentUpdateCommonSerializer(serializers.ModelSerializer):
    """
    결제내역 Update를 위한 추상적 Serializer
    """

    essetial_fields: str = ""
    compare_fields: str = ""

    def validate(self, attrs: AttrsType) -> AttrsType:
        # 필수 필드 검사
        if attrs.get(self.essetial_fields, None) is None:
            raise serializers.ValidationError(f"{self.essetial_fields}가 없습니다.")
        if attrs.get(self.compare_fields, None) is None:
            raise serializers.ValidationError(f"{self.compare_fields}가 없습니다.")
        if attrs.get(self.compare_fields) <= attrs.get(self.essetial_fields):
            return attrs
        raise serializers.ValidationError(
            f"{self.essetial_fields}가 {self.compare_fields}보다 이전입니다."
        )


class PaymentSuccessSerializer(PaymentUpdateCommonSerializer):
    """
    결제 성공 Serializer
    """

    essetial_fields: Final = "successed_at"
    compare_fields: Final = "created_at"

    class Meta:
        model: Final = Payment
        fields: Final = ("successed_at",)


class PaymentCancelSerializer(PaymentUpdateCommonSerializer):
    """
    결제 취소 Serializer
    """

    essetial_fields: Final = "canceled_at"
    compare_fields: Final = "successed_at"

    class Meta:
        model: Final = Payment
        fields: Final = ("canceled_at",)
