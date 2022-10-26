from rest_framework import serializers
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "thumbnail",
            "name",
            "price",
            "pre_sale_price",
            "is_waiting",
            "is_best",
            "is_md",
            "stock",
        )
