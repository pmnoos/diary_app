from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Entry


class EntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.entry = Entry.objects.create(
            title='Test Entry',
            content='This is a test entry.',
            author=self.user
        )

    def test_entry_creation(self):
        """Test that entries are created correctly"""
        self.assertEqual(self.entry.title, 'Test Entry')
        self.assertEqual(self.entry.author, self.user)
        self.assertTrue(self.entry.is_private)  # Default is True

    def test_entry_str_method(self):
        """Test the string representation of Entry"""
        self.assertEqual(str(self.entry), 'Test Entry by testuser')


class EntryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_entry_list_view(self):
        """Test that entry list view works"""
        response = self.client.get(reverse('entry_list'))
        self.assertEqual(response.status_code, 200)

    def test_entry_create_view_get(self):
        """Test that entry create form loads"""
        response = self.client.get(reverse('entry_create'))
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        """Test that home view works"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
