from django.core.urlresolvers import reverse
from django.test import TestCase
from cities_light.models import City, Country

from meetup.models import MeetupLocation


class MeetupLocationAboutViewTestCase(TestCase):
    def setUp(self):
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Baz', display_name='Baz', country=country)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="It's a test meetup location")

    def test_view_meetup_location_about_view(self):
        """Test Meetup Location about view for correct http response"""
        url = reverse('about_meetup_location', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/about.html')

        nonexistent_url = reverse('about_meetup_location', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)
