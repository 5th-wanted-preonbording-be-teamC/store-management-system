from django.db import models
from common.models import CommonModel


class Order(CommonModel):
    class OrderStatusChoices(models.TextChoices):
        PAYED = ("payed", "결제완료")
        SENT = ("sent", "발송완료")
        ARRIVED = ("arrived", "배송완료")

    status = models.CharField(
        max_length=7,
        choices=OrderStatusChoices.choices,
        verbose_name="상태",
        default=OrderStatusChoices.PAYED,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        verbose_name="상품",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        verbose_name="주문자",
    )
