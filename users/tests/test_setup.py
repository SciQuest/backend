from rest_framework.test import APITestCase
from django.urls import reverse
from users import models


class TestSetUp(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")

        self.user_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "test@user.com",
            "password": "12345678",
        }

        self.moderator_data = {
            "first_name": "test",
            "last_name": "moderator",
            "email": "test@moderator.com",
            "password": "12345678",
        }

        self.admin_data = {
            "first_name": "test",
            "last_name": "admin",
            "email": "test@admin.com",
            "password": "12345678",
        }

        self.admin = models.User.objects.create_superuser(
            first_name=self.admin_data["first_name"],
            last_name=self.admin_data["last_name"],
            email=self.admin_data["email"],
            password=self.admin_data["password"],
        )

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
