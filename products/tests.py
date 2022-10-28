import io
from PIL import Image
from django.conf import settings
from rest_framework.test import APITestCase
from .models import Product
from users.models import User


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


class TestProducts(APITestCase):
    def setUp(self):
        self.product, self.user, self.admin = init()

    def test_all_products(self):
        """
        상품 목록 조회 테스트
        GET /api/v1/products/
        """

        response = self.client.get("/api/v1/products/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(
            data[0]["thumbnail"], f"{settings.MEDIA_URL}{self.product.thumbnail}"
        )
        self.assertEqual(data[0]["name"], self.product.name)
        self.assertEqual(data[0]["price"], self.product.price)
        self.assertEqual(data[0]["pre_sale_price"], self.product.pre_sale_price)
        self.assertEqual(data[0]["is_waiting"], self.product.is_waiting)
        self.assertEqual(data[0]["is_best"], self.product.is_best)
        self.assertEqual(data[0]["is_md"], self.product.is_md)
        self.assertEqual(data[0]["stock"], self.product.stock)
        self.assertNotIn("description", data[0])
        self.assertNotIn("country", data[0])
        self.assertNotIn("delivery_method", data[0])
        self.assertNotIn("delivery_method", data[0])

    def test_create_product(self):
        """
        상품 생성 테스트
        POST /api/v1/products/
        """

        response = self.client.post("/api/v1/products/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        self.client.force_login(self.user)

        response = self.client.post("/api/v1/products/")
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "You do not have permission to perform this action."
        )

        self.client.force_login(self.admin)

        response = self.client.post("/api/v1/products/")
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("thumbnail", data)
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("price", data)
        self.assertIn("country", data)
        self.assertIn("delivery_method", data)

        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)

        response = self.client.post(
            "/api/v1/products/",
            {
                "thumbnail": file,
                "name": "test",
                "description": "test description",
                "price": 30000,
                "country": "Korea",
                "delivery_method": Product.ProductDeliveryMethodChoices.PARCEL,
            },
            format="multipart",
        )
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertIn("id", data)


class TestProduct(APITestCase):
    def setUp(self):
        self.product, self.user, self.admin = init()

    def test_product_notfound(self):
        """
        상품 상세 조회 NotFound 테스트
        GET /api/v1/products/{pk}/
        """

        response = self.client.get("/api/v1/products/4/")
        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["detail"], "Not found.")

    def test_one_product(self):
        response = self.client.get("/api/v1/products/1/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("id", data)
        self.assertIn("thumbnail", data)
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("price", data)
        self.assertIn("pre_sale_price", data)
        self.assertIn("is_waiting", data)
        self.assertIn("is_best", data)
        self.assertIn("is_md", data)
        self.assertIn("stock", data)
        self.assertIn("country", data)
        self.assertIn("delivery_method", data)
        self.assertIn("delivery_price", data)

    def test_update_product(self):
        response = self.client.patch("/api/v1/products/1/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        self.client.force_login(self.user)

        response = self.client.patch("/api/v1/products/1/")
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "You do not have permission to perform this action."
        )

        self.client.force_login(self.admin)

        new_name = "new_test_name"
        response = self.client.patch("/api/v1/products/1/", {"name": new_name})
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/v1/products/1/")
        data = response.json()
        self.assertEqual(data["name"], new_name)

    def test_delete_product(self):
        response = self.client.delete("/api/v1/products/1/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        self.client.force_login(self.user)

        response = self.client.delete("/api/v1/products/1/")
        data = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "You do not have permission to perform this action."
        )

        self.client.force_login(self.admin)

        response = self.client.delete("/api/v1/products/1/")
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/products/1/")
        self.assertEqual(response.status_code, 404)
