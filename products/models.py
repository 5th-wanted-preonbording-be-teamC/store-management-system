from django.db import models


class Photo(models.Model):
    file = models.ImageField(verbose_name="상품 상세 사진")
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="상품",
    )


class Product(models.Model):
    class ProductDeliveryMethodChoices(models.TextChoices):
        PARCEL = ("parcel", "택배")

    thumbnail = models.ImageField(verbose_name="썸네일")
    name = models.CharField(max_length=30, verbose_name="상품명")
    description = models.TextField(verbose_name="상품 설명")
    price = models.PositiveIntegerField(verbose_name="가격")
    pre_sale_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="세일 전 가격",
    )
    is_waiting = models.BooleanField(default=False, verbose_name="판매 대기 여부")
    is_best = models.BooleanField(default=False, verbose_name="베스트 상품 여부")
    is_md = models.BooleanField(default=False, verbose_name="MD 상품 여부")
    stock = models.PositiveIntegerField(default=0, verbose_name="재고")
    country = models.CharField(max_length=20, verbose_name="원산지")
    delivery_method = models.CharField(
        max_length=6,
        choices=ProductDeliveryMethodChoices.choices,
        verbose_name="배송방법",
    )
    delivery_price = models.PositiveIntegerField(default=0, verbose_name="배송비")
