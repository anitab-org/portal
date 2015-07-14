from django.core.urlresolvers import reverse
from django.test import TestCase
from cities_light.models import City, Country

from meetup.models import MeetupLocation


class MeetupLocationViewBaseTestCase(object):
    def setUp(self):
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Baz', display_name='Baz', country=country)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="It's a test meetup location")


class MeetupLocationAboutViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_view_meetup_location_about_view(self):
        """Test Meetup Location about view for correct http response"""
        url = reverse('about_meetup_location', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/about.html')
        self.assertEqual(response.context['meetup_location'], self.meetup_location)

        nonexistent_url = reverse('about_meetup_location', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class MeetupLocationListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_view_meetup_location_list_view(self):
        """Test Meetup Location list view for correct http response and
        all meetup locations in a list"""
        url = reverse('list_meetup_location')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_location.html")
        self.assertContains(response, "Foo Systers")
        self.assertContains(response, "google.maps.Map")

        self.meetup_location2 = MeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="It's a test meetup location")
        url = reverse('list_meetup_location')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_location.html")
        self.assertContains(response, "Foo Systers")
        self.assertContains(response, "Bar Systers")
        self.assertEqual(len(response.context['object_list']), 2)
        self.assertContains(response, "google.maps.Map")
