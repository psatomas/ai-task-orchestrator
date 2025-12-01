from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):

    def test_user_registration(self):
        url = reverse("register")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_login(self):
        user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="testpass123"
        )

        url = reverse("login")
        data = {
            "username": "loginuser",
            "password": "testpass123"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        user = User.objects.create_user(
            username="refreshuser",
            email="refresh@example.com",
            password="testpass123"
        )

        # Login to get refresh token
        login_url = reverse("login")
        login_data = {
            "username": "refreshuser",
            "password": "testpass123"
        }
        login_response = self.client.post(login_url, login_data, format="json")

        refresh_token = login_response.data["refresh"]

        # Refresh token
        refresh_url = reverse("refresh")
        refresh_data = {
            "refresh": refresh_token
        }

        refresh_response = self.client.post(refresh_url, refresh_data, format="json")

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)