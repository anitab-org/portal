from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User


class CommonViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """Test index/landing page"""
        index_url = reverse('index')
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')

    def test_contact_page(self):
        """Test contact page"""
        contact_url = reverse('contact')
        response = self.client.get(contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/contact.html')

    def test_about_us_page(self):
        """Test about us page"""
        about_us_url = reverse('about-us')
        response = self.client.get(about_us_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/about_us.html')

    def test_login_logout(self):
        """Test Login and logout functionality"""
        # Create a temporary user
        u = User.objects.create_user('admin', 'admin@admin.com', 'Qwerty@123')
        # Check response code on get request for login
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        # Log in the user
        self.client.login(username=u.username, password=u.password)
        # Check response code for logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # Log out the user
        self.client.logout()
