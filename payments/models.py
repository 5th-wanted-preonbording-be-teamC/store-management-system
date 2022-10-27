from tabnanny import verbose
from django.db import models
from common.models import CommonModel
from products.models import Product
from users.models import User


class Method(models.Model):
    """결제 수단에 대한 정보를 저장하는 테이블"""
    class PaymentMethodChoices(models.TextChoices):
        METHOD = ("신용카드", "무통장입금")
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자
    type_ = models.CharField(choices=PaymentMethodChoices.choices, verbose_name="type") # 결제수단
    company = models.CharField(max_length=20) # 카드/은행사
    number = models.CharField(max_length=20) # 카드/계좌번호


class Payment(CommonModel):
    """결제에 대한 정보를 저장하는 테이블"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # 상품
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # 결제자
    price = models.PositiveIntegerField(null=False) # 상품가격
    delivery_fee = models.PositiveIntegerField(null=False) # 배송비
    amount = models.PositiveIntegerField(null=False) # 최종결제금액 (상품가격 + 배송비)
    payment_method = models.ForeignKey(Method, on_delete=models.SET_NULL, null=True) # 결제수단
    delivery_address = models.TextField(null=True, blank=True) # 배송지 주소 및 메모
    successed_at = models.DateTimeField(null=True) # 결제 성공 시간 (null이면 결제 실패)
    canceled_at = models.DateTimeField(null=True) # 결제 취소 시간 (null이면 결제 유지 중)
    shiped_at = models.DateTimeField(null=True) # 배송 시작 시간 (null이면 배송 전)
    deliveried_at = models.DateTimeField(null=True) # 배송 완료 시간 (null이면 배송 미완료)
