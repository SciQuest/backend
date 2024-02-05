from rest_framework import status
from users.tests.test_setup import TestSetUp
from users import models


class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["role"], models.Role.USER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_login_without_register(self):
        response = self.client.post(self.token_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_login_correctly(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.token_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_login_correctly(self):
        response = self.client.post(self.token_url, self.admin_data, format="json")
        self.assertEqual(self.admin.role, models.Role.ADMIN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_moderator(self):
        admin_token = self.client.post(
            self.token_url, self.admin_data, format="json"
        ).data["access"]
        response = self.client.post(
            self.register_url,
            self.moderator_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {admin_token}",
        )
        self.assertEqual(response.data["role"], models.Role.MODERATOR)
