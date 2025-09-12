from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
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
            author=self.user,
            date=timezone.now().date()
        )

    def test_entry_creation(self):
        """Test that entries are created correctly"""
        self.assertEqual(self.entry.title, 'Test Entry')
        self.assertEqual(self.entry.author, self.user)
        self.assertTrue(self.entry.is_private)  # Default is True

    def test_entry_str_method(self):
        """Test the string representation of Entry"""
        self.assertEqual(str(self.entry), 'Test Entry by testuser')

    def test_entry_ordering(self):
        """Test that entries are ordered by date"""
        yesterday = timezone.now().date() - timedelta(days=1)
        entry2 = Entry.objects.create(
            title='Second Entry',
            content='This is the second entry.',
            author=self.user,
            date=yesterday
        )
        entries = Entry.objects.all()
        self.assertEqual(entries[0], self.entry)  # Today's entry first (newer date)


class EntryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_home_view(self):
        """Test that home view works"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_entry_list_requires_login(self):
        """Test that entry list requires authentication"""
        response = self.client.get('/entries/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_entry_list_view_authenticated(self):
        """Test that entry list view works when logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/entries/')
        self.assertEqual(response.status_code, 200)
