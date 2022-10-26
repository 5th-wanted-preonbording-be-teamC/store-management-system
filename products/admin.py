from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "is_waiting",
        "is_best",
        "is_md",
        "stock",
    )
