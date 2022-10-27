from rest_framework import serializers
from .models import Order
from products.serializers import ProductListSerializer
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "status",
            "product",
            "user",
            "payment",
        )
