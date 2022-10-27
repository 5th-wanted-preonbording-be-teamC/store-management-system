from rest_framework import serializers
from .models import Order
from products.serializers import ProductListSerializer
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "status",
            "products",
            "user",
            "payment",
        )
