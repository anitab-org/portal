from django.core.urlresolvers import reverse
from django.test import TestCase, Client


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
