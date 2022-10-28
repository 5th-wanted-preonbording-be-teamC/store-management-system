from rest_framework.test import APITestCase
from users.models import User
from products.models import Product


def init():
    """초기 데이터베이스 설정"""
    product = Product.objects.create(
        thumbnail="1",
        name="테스트상품",
        description="테스트설명",
        price=35000,
        pre_sale_price=40000,
        is_waiting=False,
        is_best=True,
        is_md=True,
        stock=300,
        country="Korea",
        delivery_method=Product.ProductDeliveryMethodChoices.PARCEL,
        delivery_price=3000,
    )
    user = User.objects.create(user_id="test")
    user = user
    admin = User.objects.create(user_id="admin", is_staff=True)
    admin = admin

    return product, user, admin


class TestOrders(APITestCase):
    def setUp(self):
        self.product, self.user, self.admin = init()

    def test_all_orders(self):
        """
        주문 목록 조회 테스트
        GET /api/v1/orders/
        """
        response = self.client.get("/api/v1/orders/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        self.client.force_login(self.user)

        response = self.client.get("/api/v1/orders/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "You do not have permission to perform this action."
        )

        self.client.force_login(self.admin)

        response = self.client.get("/api/v1/orders/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
