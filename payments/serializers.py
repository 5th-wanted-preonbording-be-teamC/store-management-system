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


class PaymentSuccessSerializer(PaymentUpdateCommonSerializer):
    """
    결제 성공 Serializer
    """
    essetial_fields = "successed_at"
    compare_fields = "created_at"

    class Meta:
        model = Payment
        fields = ("successed_at",)


class PaymentCancelSerializer(PaymentUpdateCommonSerializer):
    """
    결제 취소 Serializer
    """
    essetial_fields = "canceled_at"
    compare_fields = "successed_at"

    def additional_validate(validate):
        def wrapper(self, attrs):
            if attrs.get("shiped_at", None) is not None:
                # 배송중인 경우 취소 불가
                raise serializers.ValidationError("배송이 시작된 상품은 취소할 수 없습니다.")
            return validate(self, attrs)
        return wrapper

    class Meta:
        model = Payment
        fields = ("canceled_at",)


class PaymentShipSerializer(PaymentUpdateCommonSerializer):
    """
    배송 시작 Serializer
    """
    essetial_fields = "shiped_at"
    compare_fields = "successed_at"

    def additional_validate(validate):
        def wrapper(self, attrs):
            if attrs.get("canceled_at", None) is not None:
                # 이미 취소된 경우 배송 불가
                raise serializers.ValidationError("이미 취소된 상품은 배송할 수 없습니다.")
            return validate(self, attrs)
        return wrapper

    class Meta:
        model = Payment
        fields = ("shiped_at",)


class PaymentDeliverySerializer(PaymentUpdateCommonSerializer):
    """
    배송 시작 Serializer
    """
    essetial_fields = "deliveried_at"
    compare_fields = "shiped_at"

    class Meta:
        model = Payment
        fields = ("deliveried_at",)


class PaymentDeliveryAddressSerializer(serializers.ModelSerializer):
    """
    배송지 변경 Serializer
    """
    def validate(self, attrs):
        if attrs.get("shiped_at") is not None:
            # 배송이 시작된 경우 배송지 변경 불가
            raise serializers.ValidationError("배송이 시작된 상품은 배송지를 변경할 수 없습니다.")
        return attrs

    class Meta:
        model = Payment
        fields = ("delivery_address",)
