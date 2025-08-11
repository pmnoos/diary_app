from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsTest(TestCase):
    def test_signup_view_get(self):
        """Test that signup page loads"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        """Test that login page loads"""
        response = self.client.get(reverse('login'))
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
