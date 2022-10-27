from django.db import models
from common.models import CommonModel


class Order(CommonModel):

    """주문 테이블"""

    class OrderStatusChoices(models.TextChoices):
        PAYED = ("payed", "결제완료")
        SENT = ("sent", "발송완료")
        ARRIVED = ("arrived", "배송완료")
        CANCEL = ("cancel", "결제취소")
        REFUND = ("refund", "환불")

    status = models.CharField(
        max_length=7,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PAYED,
        verbose_name="상태",
    )
    delivery_address = models.TextField(verbose_name="배송지 주소")
    products = models.ManyToManyField(
        "products.Product",
        related_name="orders",
        verbose_name="주문상품",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        verbose_name="주문자",
    )
    payment = models.OneToOneField(
        "payments.Payment",
        on_delete=models.SET_NULL,
        related_name="order",
        null=True,
        blank=True,
        verbose_name="결재",
    )

    def __str__(self):
        return f"{self.user}의 상품 주문"
