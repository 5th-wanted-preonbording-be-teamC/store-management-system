from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    결제내역 Serializer
    """
    class Meta:
        model = Payment
        fields = (
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
            "created_at",
            "updated_at",
        )

