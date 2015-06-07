from django.test import TestCase
from cities_light.models import City, Country

from meetup.models import MeetupLocation


class MeetupLocationModelTestCase(TestCase):
    def setUp(self):
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo", slug="foo", location=self.location,
            description="It's a test location")

    def test_str(self):
        """Test MeetupLocation object str/unicode representation"""
        self.assertEqual(str(self.meetup_location),
                         "Foo Systers")
