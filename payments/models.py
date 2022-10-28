from typing import Tuple
from django.db import models
from common.models import CommonModel
from products.models import Product
from users.models import User


class Method(models.Model):
    """결제 수단에 대한 정보를 저장하는 테이블"""

    class PaymentMethodChoices(models.TextChoices):
        CARD: Tuple[str] = ("card", "신용카드")
        DEPOSIT: Tuple[str] = ("deposit", "무통장입금")

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자
    type: models.CharField = models.CharField(
        choices=PaymentMethodChoices.choices,
        max_length=8,
        verbose_name="type",
    )  # 결제수단
    company: models.CharField = models.CharField(max_length=20)  # 카드/은행사
    number: models.CharField = models.CharField(max_length=20)  # 카드/계좌번호


class Payment(CommonModel):
    """결제에 대한 정보를 저장하는 테이블"""

    product: models.ForeignKey = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True
    )  # 상품
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )  # 결제자
    price: models.PositiveIntegerField = models.PositiveIntegerField(null=False)  # 상품가격
    delivery_fee: models.PositiveIntegerField = models.PositiveIntegerField(
        null=False
    )  # 배송비
    amount: models.PositiveIntegerField = models.PositiveIntegerField(
        null=False
    )  # 최종결제금액 (상품가격 + 배송비)
    payment_method: models.ForeignKey = models.ForeignKey(
        Method, on_delete=models.SET_NULL, null=True
    )  # 결제수단
    successed_at: models.DateTimeField = models.DateTimeField(
        null=True
    )  # 결제 성공 시간 (null이면 결제 실패)
    canceled_at: models.DateTimeField = models.DateTimeField(
        null=True
    )  # 결제 취소 시간 (null이면 결제 유지 중)
