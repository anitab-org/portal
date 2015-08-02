from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import timedelta
from cities_light.models import City, Country


from meetup.forms import AddMeetupForm
from meetup.models import Meetup, MeetupLocation
from users.models import SystersUser


class AddMeetupFormTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Baz', display_name='Baz', country=country)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="It's a test meetup location")

    def test_add_meetup_form(self):
        """Test add Meetup form"""
        invalid_data = {'title': 'abc', 'date': timezone.now().date()}
        form = AddMeetupForm(data=invalid_data, created_by=self.systers_user,
                             meetup_location=self.meetup_location)
        self.assertFalse(form.is_valid())

        date = (timezone.now() + timedelta(2)).date()
        time = timezone.now().time()
        data = {'title': 'Foo', 'slug': 'foo', 'date': date, 'time': time,
                'description': "It's a test meetup."}
        form = AddMeetupForm(data=data, created_by=self.systers_user,
                             meetup_location=self.meetup_location)
        self.assertTrue(form.is_valid())
        form.save()
        new_meetup = Meetup.objects.get()
        self.assertTrue(new_meetup.title, 'Foo')
        self.assertTrue(new_meetup.created_by, self.systers_user)
        self.assertTrue(new_meetup.meetup_location, self.meetup_location)
