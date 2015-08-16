from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone
from cities_light.models import City, Country

from meetup.models import Meetup, MeetupLocation
from users.models import SystersUser


class MeetupLocationViewBaseTestCase(object):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
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


class MeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(MeetupViewTestCase, self).setUp()
        self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                            date=timezone.now().date(),
                                            time=timezone.now().time(),
                                            description='This is test Meetup',
                                            meetup_location=self.meetup_location,
                                            created_by=self.systers_user,
                                            last_updated=timezone.now())

    def test_view_meetup(self):
        """Test Meetup view for correct response"""
        url = reverse('view_meetup', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/meetup.html')
        self.assertEqual(response.context['meetup_location'], self.meetup_location)
        self.assertEqual(response.context['meetup'], self.meetup)

        nonexistent_url = reverse('view_meetup', kwargs={'slug': 'foo1',
                                  'meetup_slug': 'bazbar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        self.meetup_location2 = MeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="It's a test meetup location")
        incorrect_pair_url = reverse('view_meetup', kwargs={'slug': 'bar',
                                     'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(incorrect_pair_url)
        self.assertEqual(response.status_code, 404)


class MeetupLocationMembersViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_view_meetup_location_members_view(self):
        """Test Meetup Location members view for correct http response"""
        url = reverse('members_meetup_location', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/members.html')

        nonexistent_url = reverse('members_meetup_location', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class AddMeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_add_meetup_view(self):
        """Test GET request to add a new meetup"""
        url = reverse('add_meetup', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/add_meetup.html')

    def test_post_add_meetup_view(self):
        """Test POST request to add a new meetup"""
        url = reverse("add_meetup", kwargs={'slug': 'foo'})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        date = (timezone.now() + timezone.timedelta(2)).date()
        time = timezone.now().time()
        data = {'title': 'BarTest', 'slug': 'bartest', 'date': date, 'time': time,
                'description': "It's a test meetup."}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        new_meetup = Meetup.objects.get()
        self.assertTrue(new_meetup.title, 'BarTest')
        self.assertTrue(new_meetup.created_by, self.systers_user)
        self.assertTrue(new_meetup.meetup_location, self.meetup_location)


class DeleteMeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(DeleteMeetupViewTestCase, self).setUp()
        self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                            date=timezone.now().date(),
                                            time=timezone.now().time(),
                                            description='This is test Meetup',
                                            meetup_location=self.meetup_location,
                                            created_by=self.systers_user,
                                            last_updated=timezone.now())
        self.client = Client()

    def test_get_delete_meetup_view(self):
        """Test GET to confirm deletion of meetup"""
        url = reverse("delete_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_meetup_view(self):
        """Test POST to delete a meetup"""
        url = reverse("delete_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertSequenceEqual(Meetup.objects.all(), [])


class PastMeetupListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(PastMeetupListViewTestCase, self).setUp()
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())

    def test_view_past_meetup_list_view(self):
        """Test Past Meetup list view for correct http response and
        all past meetups in a list"""
        url = reverse('past_meetups', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/past_meetups.html")
        self.assertEqual(len(response.context['meetup_list']), 0)
