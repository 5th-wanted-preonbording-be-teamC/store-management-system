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


class PaymentUpdateCommonSerializer(serializers.ModelSerializer):
    """
    결제내역 Update를 위한 추상적 Serializer
    """
    essetial_fields = ""
    compare_fields = ""
    def additional_validate(validate):
        # 취소 등 추가 검사가 필요한 경우, 이곳에서 추가 검사
        def wrapper(self, attrs):
            return validate(self, attrs)
        return wrapper
    
    @additional_validate
    def validate(self, attrs):
        # 필수 필드 검사
        if attrs.get(self.essetial_fields, None) is None:
            raise serializers.ValidationError(f"{self.essetial_fields}가 없습니다.")
        if attrs.get(self.compare_fields, None) is None:
            raise serializers.ValidationError(f"{self.compare_fields}가 없습니다.")
        if attrs.get(self.compare_fields) <= attrs.get(self.essetial_fields):
            return attrs
        raise serializers.ValidationError(f"{self.essetial_fields}가 {self.compare_fields}보다 이전입니다.")

