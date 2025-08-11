from django.test import TestCase, Client
from django.contrib.auth.models import User


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view_get(self):
        """Test that signup page loads"""
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        """Test that login page loads"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):
        """Test that users can be created"""
        user_count = User.objects.count()
        User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_user_login(self):
        """Test that users can log in"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)
