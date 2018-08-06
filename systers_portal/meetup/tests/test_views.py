from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone
from cities_light.models import City, Country
from django.contrib.contenttypes.models import ContentType

from meetup.models import (Meetup, MeetupLocation, Rsvp, SupportRequest, RequestMeetupLocation,
                           RequestMeetup)
from users.models import SystersUser
from common.models import Comment
from rest_framework.test import APITestCase
import json


class MeetupLocationViewBaseTestCase(object):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar',
                                             email='user@test.com')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Baz', display_name='Baz', country=country)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="It's a test meetup location", sponsors="BarBaz", leader=self.systers_user)
        self.meetup_location.members.add(self.systers_user)
        self.meetup_location.moderators.add(self.systers_user)
        self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                            date=timezone.now().date(),
                                            time=timezone.now().time(),
                                            description='This is test Meetup',
                                            meetup_location=self.meetup_location,
                                            created_by=self.systers_user,
                                            last_updated=timezone.now())


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


class AllUpcomingMeetupsViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_view_all_upcoming_meetups_list_view(self):
        """Test All Upcoming Meetups list view for correct http response"""
        url = reverse('all_upcoming_meetups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_meetup.html")
        self.assertContains(response, "Foo Systers")
        self.assertContains(response, "Foo Bar Baz")
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(len(response.context['meetup_list']), 1)

        self.meetup_location2 = MeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="It's a test meetup location", leader=self.systers_user)
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location2,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())
        url = reverse('all_upcoming_meetups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_meetup.html")
        self.assertContains(response, "Foo Systers")
        self.assertContains(response, "Bar Systers")
        self.assertContains(response, "Foo Bar Baz")
        self.assertContains(response, "Bar Baz")
        self.assertEqual(len(response.context['object_list']), 2)
        self.assertEqual(len(response.context['meetup_list']), 2)


class MeetupLocationListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_view_meetup_location_list_view(self):
        """Test Meetup Location list view for correct http response,
        all meetup locations in a list and all upcoming meetups"""
        url = reverse('list_meetup_location')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_location.html")
        self.assertContains(response, "Foo Systers")
        self.assertContains(response, "Foo Bar Baz")
        self.assertContains(response, "google.maps.Map")
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(len(response.context['meetup_list']), 1)

        self.meetup_location2 = MeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="It's a test meetup location", leader=self.systers_user)
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location2,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())
        url = reverse('list_meetup_location')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_location.html")
        self.assertContains(response, "Foo Systers")
        self.assertContains(response, "Bar Systers")
        self.assertContains(response, "Foo Bar Baz")
        self.assertContains(response, "Bar Baz")
        self.assertEqual(len(response.context['object_list']), 2)
        self.assertEqual(len(response.context['meetup_list']), 2)
        self.assertContains(response, "google.maps.Map")


class MeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
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
            description="It's a test meetup location", leader=self.systers_user)
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
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
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
        new_meetup = Meetup.objects.get(slug='bartest')
        self.assertTrue(new_meetup.title, 'BarTest')
        self.assertTrue(new_meetup.created_by, self.systers_user)
        self.assertTrue(new_meetup.meetup_location, self.meetup_location)


class RequestMeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_request_meetup_view(self):
        """Test GET request to request a new meetup"""
        url = reverse('request_meetup', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/request_new_meetup.html')

    def test_post_request_meetup_view(self):
        """Test POST request to request a new meetup"""
        url = reverse("request_meetup", kwargs={'slug': 'foo'})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        date = (timezone.now() + timezone.timedelta(2)).date()
        time = timezone.now().time()
        data = {'title': 'BarTest', 'slug': 'bartest', 'date': date, 'time': time,
                'description': "It's a test meetup."}
        response = self.client.post(url, data=data, created_by=self.systers_user,
                                    meetup_location=self.meetup_location)
        self.assertEqual(response.status_code, 302)
        new_meetup_request = RequestMeetup.objects.get(slug='bartest')
        self.assertTrue(new_meetup_request.title, 'BarTest')
        self.assertTrue(new_meetup_request.created_by, self.systers_user)
        self.assertTrue(new_meetup_request.meetup_location, self.meetup_location)


class NewMeetupRequestsListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(NewMeetupRequestsListViewTestCase, self).setUp()
        self.meetup_request1 = RequestMeetup.objects.create(
            title="Bar Talk", slug="bar", date=timezone.now().date(), time=timezone.now().time(),
            description="This is a test meetup location request1", created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.meetup_request2 = RequestMeetup.objects.create(
            title="Foo Talk", slug="foo", date=timezone.now().date(), time=timezone.now().time(),
            description="This is a test meetup location request2", created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_view_new_meetup_location_requests_list_view(self):
        """Test Meetup Requests list view for correct http response and
        all meetup requests in a list"""
        url = reverse('new_meetup_requests', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Testing after logggin in - normal user
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Testing after logging in - Organizer of the Meetup Location
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "meetup/new_meetup_requests.html")
        self.assertContains(response, "Foo Talk")
        self.assertSequenceEqual(RequestMeetup.objects.filter(
            is_approved=False), [self.meetup_request1, self.meetup_request2])
        self.assertContains(response, "Requested by")


class ViewMeetupRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(ViewMeetupRequestViewTestCase, self).setUp()
        self.meetup_request = RequestMeetup.objects.create(
            title="Foo Talk", slug="bar", date=timezone.now().date(), time=timezone.now().time(),
            description="This is a test meetup location request", created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_view_meetup_request_view(self):
        """Test Meetup Request view for correct response"""
        # Test without logging in
        url = reverse('view_meetup_request', kwargs={'slug': 'foo', 'meetup_slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test after logging in - normal user
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test after logging in - moderator
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'meetup/view_new_meetup_request.html')
        self.assertEqual(
            response.context['meetup_request'], self.meetup_request)


class ApproveRequestMeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(ApproveRequestMeetupViewTestCase, self).setUp()
        self.meetup_request = RequestMeetup.objects.create(
            title="Foo Talk", slug="bar", date=timezone.now().date(), time=timezone.now().time(),
            description="This is a test meetup location request", created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_approve_request_meetup_view_base(self):
        url = reverse('approve_meetup_request',
                      kwargs={'meetup_slug': 'bar', 'slug': 'foo'})
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if accessed by a Organizer
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('meetup/foo/bar/'))
        # Test for non existent url
        nonexistent_url = reverse('approve_meetup_request',
                                  kwargs={'slug': 'foo', 'meetup_slug': 'carr'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_approve_request_meetup_view_slug(self):
        """Test if slug already exists in Meetup Location objects, redirect to edit page."""
        url = reverse('approve_meetup_request',
                      kwargs={'meetup_slug': 'bar', 'slug': 'foo'})
        Meetup.objects.create(title='Foo Bar Baz', slug='bar',
                              date=timezone.now().date(),
                              time=timezone.now().time(),
                              description='This is test Meetup',
                              meetup_location=self.meetup_location,
                              created_by=self.systers_user,
                              last_updated=timezone.now())
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('meetup/foo/view_meetup_requests/'))


class RejectMeetupRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(RejectMeetupRequestViewTestCase, self).setUp()
        self.meetup_request = RequestMeetup.objects.create(
            title="Foo Talk", slug="bar", date=timezone.now().date(), time=timezone.now().time(),
            description="This is a test meetup request", created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_get_reject_request_meetup_view(self):
        url = reverse('reject_meetup_request', kwargs={'slug': 'foo', 'meetup_slug': 'bar'})
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if accessed by a superuser
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "meetup/confirm_reject_request_meetup.html")
        # Test for non existent url
        nonexistent_url = reverse('reject_meetup_request',
                                  kwargs={'slug': 'foo', 'meetup_slug': 'barr'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_post_reject_request_meetup_location_view(self):
        url = reverse('reject_meetup_request', kwargs={'slug': 'foo', 'meetup_slug': 'bar'})
        # Test without logging in
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foobar', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # Test if superuser posts
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('view_meetup_requests/'))
        # Test non existent url
        nonexistent_url = reverse('reject_meetup_request',
                                  kwargs={'slug': 'foo', 'meetup_slug': 'barr'})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class DeleteMeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(DeleteMeetupViewTestCase, self).setUp()
        self.meetup2 = Meetup.objects.create(title='Fooba', slug='fooba',
                                             date=timezone.now().date(),
                                             time=timezone.now().time(),
                                             description='This is test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())
        self.client = Client()

    def test_get_delete_meetup_view(self):
        """Test GET to confirm deletion of meetup"""
        url = reverse("delete_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'fooba'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_meetup_view(self):
        """Test POST to delete a meetup"""
        url = reverse("delete_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'fooba'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # One meetup deleted, another meetup left initialized in
        # MeetupLocationViewBaseTestCase
        self.assertSequenceEqual(Meetup.objects.all(), [self.meetup])


class EditMeetupView(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_edit_meetup_view(self):
        """Test GET edit meetup"""
        wrong_url = reverse("edit_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'foo'})
        response = self.client.get(wrong_url)
        self.assertEqual(response.status_code, 403)

        url = reverse("edit_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/edit_meetup.html')

    def test_post_edit_meetup_view(self):
        """Test POST edit meetup"""
        wrong_url = reverse("edit_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'foo'})
        response = self.client.post(wrong_url)
        self.assertEqual(response.status_code, 403)

        url = reverse("edit_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        date = (timezone.now() + timezone.timedelta(2)).date()
        time = timezone.now().time()
        data = {'title': 'BarTes', 'slug': 'bartes', 'date': date, 'time': time,
                'description': "It's a edit test meetup."}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/meetup/foo/bartes/'))


class UpcomingMeetupsViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(UpcomingMeetupsViewTestCase, self).setUp()
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())

    def test_view_upcoming_meetup_list_view(self):
        """Test Upcoming Meetup list view for correct http response and
        all upcoming meetups in a list"""
        url = reverse('upcoming_meetups', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/upcoming_meetups.html")
        self.assertContains(response, "Foo Bar Baz")
        self.assertContains(response, "Bar Baz")
        self.assertEqual(len(response.context['meetup_list']), 2)


class PastMeetupListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(PastMeetupListViewTestCase, self).setUp()
        # a future meetup. This should not show up under 'past meetups'.
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())
        # a past meetup. This should show up under 'past meetups'.
        self.meetup3 = Meetup.objects.create(title='Foo Baz', slug='foobar',
                                             date=(timezone.now() - timezone.timedelta(2)).date(),
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
        self.assertEqual(len(response.context['meetup_list']), 1)


class MeetupLocationSponsorsViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_view_meetup_location_sponsors_view(self):
        """Test Meetup Location sponsors view for correct http response"""
        url = reverse('sponsors_meetup_location', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/sponsors.html")
        self.assertEqual(response.context['meetup_location'], self.meetup_location)

        nonexistent_url = reverse('sponsors_meetup_location', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class RemoveMeetupLocationMemberViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(RemoveMeetupLocationMemberViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        self.meetup_location.members.add(self.systers_user2)
        self.meetup_location.moderators.add(self.systers_user2)
        self.user3 = User.objects.create_user(username='bar', password='barbar')
        self.systers_user3 = SystersUser.objects.get(user=self.user3)
        self.meetup_location.members.add(self.systers_user3)

    def test_view_remove_meetup_location_member_view(self):
        """
        Test remove Meetup Location member view for 3 cases:

        * removing only a member
        * removing one of two members who are moderators
        * removing member who is the only moderator
        """
        url = reverse("remove_member_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse("remove_member_meetup_location",
                                  kwargs={'slug': 'foo', 'username': 'barbaz'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        url = reverse("remove_member_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'bar'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/members/')
        self.assertEqual(len(self.meetup_location.members.all()), 2)

        url = reverse("remove_member_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/members/')
        self.assertEqual(len(self.meetup_location.members.all()), 1)
        self.assertEqual(len(self.meetup_location.moderators.all()), 1)

        url = reverse("remove_member_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'foo'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/members/')
        self.assertEqual(len(self.meetup_location.members.all()), 1)
        self.assertEqual(len(self.meetup_location.moderators.all()), 1)


class AddMeetupLocationMemberViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(AddMeetupLocationMemberViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_get_add_meetup_location_member_view(self):
        url = reverse("add_member_meetup_location", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/add_member.html')

    def test_post_add_meetup_location_member_view(self):
        url = reverse("add_member_meetup_location", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        username = self.user2.get_username()
        data = {'username': username}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)
        self.assertTrue(response.url.endswith('/meetup/foo/members/'))
        self.assertEqual(response.status_code, 302)


class RemoveMeetupLocationModeratorViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(RemoveMeetupLocationModeratorViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        self.meetup_location.members.add(self.systers_user2)
        self.meetup_location.moderators.add(self.systers_user2)

    def test_view_remove_meetup_location_moderator_view(self):
        """
        Test remove Meetup Location moderator view for 2 cases:

        * remove one of two moderators
        * remove the only moderator
        """
        url = reverse("remove_moderator_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse("remove_moderator_meetup_location",
                                  kwargs={'slug': 'foo', 'username': 'barbaz'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        url = reverse("remove_moderator_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/members/')
        self.assertEqual(len(self.meetup_location.members.all()), 2)
        self.assertEqual(len(self.meetup_location.moderators.all()), 1)

        url = reverse("remove_moderator_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'foo'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/members/')
        self.assertEqual(len(self.meetup_location.members.all()), 2)
        self.assertEqual(len(self.meetup_location.moderators.all()), 1)


class MakeMeetupLocationModeratorViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(MakeMeetupLocationModeratorViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        self.meetup_location.members.add(self.systers_user2)

    def test_view_make_meetup_location_moderator_view(self):
        """Test make Meetup Location moderator view for correct http response"""
        url = reverse("make_moderator_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse("make_moderator_meetup_location",
                                  kwargs={'slug': 'foo', 'username': 'barbaz'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        url = reverse("make_moderator_meetup_location",
                      kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/members/')
        self.assertEqual(len(self.meetup_location.members.all()), 2)
        self.assertEqual(len(self.meetup_location.moderators.all()), 2)


class JoinMeetupLocationViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(JoinMeetupLocationViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        self.meetup_location.join_requests.add(self.systers_user2)
        self.user3 = User.objects.create_user(username='bar', password='barbar')
        self.systers_user3 = SystersUser.objects.get(user=self.user3)

    def test_view_join_meetup_location_view(self):
        """
        Test join meetup location view for three cases:

        * User who is joining meetup location
        * User who has already requested to join
        * User who is already a member
        """
        url = reverse('join_meetup_location', kwargs={'slug': 'foo', 'username': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        wrong_url = reverse('join_meetup_location', kwargs={'slug': 'foo', 'username': 'foba'})
        response = self.client.get(wrong_url)
        self.assertEqual(response.status_code, 404)

        url = reverse('join_meetup_location', kwargs={'slug': 'foo', 'username': 'bar'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/about/')
        self.assertEqual(len(self.meetup_location.join_requests.all()), 2)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Your request to join meetup location Foo Systers has been sent.'
                in message.message)

        url = reverse('join_meetup_location', kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/about/')
        self.assertEqual(len(self.meetup_location.join_requests.all()), 2)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'You have already requested to join meetup location Foo Systers.'
                in message.message)

        url = reverse('join_meetup_location', kwargs={'slug': 'foo', 'username': 'foo'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/about/')
        self.assertEqual(len(self.meetup_location.join_requests.all()), 2)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "warning")
            self.assertTrue(
                'You are already a member of meetup location Foo Systers.'
                in message.message)


class MeetupLocationJoinRequestsViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(MeetupLocationJoinRequestsViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        self.meetup_location.join_requests.add(self.systers_user2)

    def test_view_meetup_location_join_requests_view(self):
        """Test meetup location join requests view for correct http response"""
        url = reverse('join_requests_meetup_location', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse('join_requests_meetup_location', kwargs={'slug': 'baaa'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        url = reverse('join_requests_meetup_location', kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/join_requests.html")
        self.assertEqual(len(response.context['requests']), 1)


class ApproveMeetupLocationJoinRequestsViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(ApproveMeetupLocationJoinRequestsViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        self.meetup_location.join_requests.add(self.systers_user2)

    def test_view_approve_meetup_location_join_requests_view(self):
        """Test approve meetup location join requests view for correct http response"""
        url = reverse('approve_join_request_meetup_location',
                      kwargs={'slug': 'foo', 'username': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse('approve_join_request_meetup_location',
                                  kwargs={'slug': 'foo', 'username': 'foba'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        url = reverse('approve_join_request_meetup_location',
                      kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/join_requests/')
        self.assertEqual(len(self.meetup_location.join_requests.all()), 0)
        self.assertEqual(len(self.meetup_location.members.all()), 2)


class RejectMeetupLocationJoinRequestsViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(RejectMeetupLocationJoinRequestsViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        self.meetup_location.join_requests.add(self.systers_user2)

    def test_view_reject_meetup_location_join_requests_view(self):
        """Test reject meetup location join requests view for correct http response"""
        url = reverse('reject_join_request_meetup_location',
                      kwargs={'slug': 'foo', 'username': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse('reject_join_request_meetup_location',
                                  kwargs={'slug': 'foo', 'username': 'foba'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        url = reverse('reject_join_request_meetup_location',
                      kwargs={'slug': 'foo', 'username': 'baz'})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/join_requests/')
        self.assertEqual(len(self.meetup_location.join_requests.all()), 0)
        self.assertEqual(len(self.meetup_location.members.all()), 1)


class AddMeetupLocationViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_add_meetup_location_view(self):
        """Test GET request to add a new meetup location"""
        url = reverse('add_meetup_location')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/add_meetup_location.html')

    def test_post_add_meetup_location_view(self):
        """Test POST request to add a new meetup location"""
        url = reverse('add_meetup_location')
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        url = reverse('add_meetup_location')
        data = {'name': 'Bar Systers', 'slug': 'bar', 'location': self.location.id,
                'description': "It's a new meetup location", 'sponsors': 'BaaBaa'}
        response = self.client.post(url, data=data, user=self.systers_user)
        self.assertEqual(response.status_code, 302)
        new_meetup_location = MeetupLocation.objects.get(slug='bar')
        self.assertTrue(new_meetup_location.name, 'Bar Systers')


class RequestMeetupLocationViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_add_meetup_location_view(self):
        """Test GET request to add a new meetup location"""
        url = reverse('request_meetup_location')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'meetup/request_new_meetup_location.html')

    def test_post_add_meetup_location_view(self):
        """Test POST request to add a new meetup location"""
        url = reverse('request_meetup_location')
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        data = {'name': 'Bar Systers', 'slug': 'bar', 'location': self.location.id,
                'description': "It's a new meetup location"}
        response = self.client.post(url, data=data, user=self.systers_user)
        self.assertEqual(response.status_code, 302)
        new_meetup_location_request = RequestMeetupLocation.objects.get(
            slug='bar')
        self.assertTrue(new_meetup_location_request.name, 'Bar Systers')


class NewMeetupLocationRequestsListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(NewMeetupLocationRequestsListViewTestCase, self).setUp()
        self.meetup_location_request1 = RequestMeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="This is a test meetup location request1", user=self.systers_user)
        self.meetup_location_request2 = RequestMeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="This is a test meetup location request2", user=self.systers_user)
        self.staff_user = User.objects.create_superuser(username='foobar', password='foobar',
                                                        email='foobar@test.com')
        self.staff_systers_user = SystersUser.objects.get(user=self.staff_user)

    def test_view_new_meetup_location_requests_list_view(self):
        """Test Meetup Location Requests list view for correct http response and
        all meetup location requests in a list"""
        url = reverse('new_meetup_location_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Testing after logggin in - normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Testing after logging in - staff user
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "meetup/new_meetup_location_requests.html")
        self.assertContains(response, "Foo Systers")
        self.assertSequenceEqual(RequestMeetupLocation.objects.filter(
            is_approved=False), [self.meetup_location_request1, self.meetup_location_request2])
        self.assertContains(response, "Requested by")


class ViewMeetupLocationRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(ViewMeetupLocationRequestViewTestCase, self).setUp()
        self.meetup_location_request = RequestMeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="This is a test meetup location request",
            user=self.systers_user)
        self.staff_user = User.objects.create_superuser(username='foobar', password='foobar',
                                                        email='foobar@test.com')
        self.staff_systers_user = SystersUser.objects.get(user=self.staff_user)

    def test_view_support_request_view(self):
        """Test Meetup Location Request view for correct response"""
        # Test without logging in
        url = reverse('view_meetup_location_request', kwargs={'slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test after logging in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'meetup/view_new_meetup_location_request.html')
        self.assertEqual(
            response.context['meetup_location_request'], self.meetup_location_request)


class ApproveRequestMeetupLocationViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(ApproveRequestMeetupLocationViewTestCase, self).setUp()
        self.meetup_location_request = RequestMeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="This is a test meetup location request",
            user=self.systers_user)
        self.staff_user = User.objects.create_superuser(username='foobar', password='foobar',
                                                        email='foobar@test.com')
        self.staff_systers_user = SystersUser.objects.get(user=self.staff_user)
        country = Country.objects.create(name='Barbar', continent='AS')
        self.location2 = City.objects.create(
            name='BazBaz', display_name='Bazz', country=country)

    def test_approve_request_meetup_location_view_base(self):
        url = reverse('approve_meetup_location_request',
                      kwargs={'slug': 'bar'})
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if accessed by a superuser
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('meetup/bar/about/'))
        # Test for non existent url
        nonexistent_url = reverse('approve_meetup_location_request',
                                  kwargs={'slug': 'foo'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_approve_request_meetup_location_view_name(self):
        # Test if name of request already exists in Meetup Location objects, redirect to edit page.
        url = reverse('approve_meetup_location_request',
                      kwargs={'slug': 'bar'})
        MeetupLocation.objects.create(
            name="Bar Systers", slug="fooo", location=self.location2,
            description="It's a test meetup location", sponsors="BarBaz",
            leader=self.staff_systers_user)
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('view-requests/'))

    def test_approve_request_meetup_location_view_slug(self):
        """Test if slug already exists in Meetup Location objects, redirect to edit page."""
        url = reverse('approve_meetup_location_request',
                      kwargs={'slug': 'bar'})
        MeetupLocation.objects.create(
            name="Fooo Systers", slug="bar", location=self.location2,
            description="It's a test meetup location", sponsors="BarBaz",
            leader=self.staff_systers_user)
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('view-requests/'))

    def test_approve_request_meetup_location_view_location(self):
        """Test if slug already exists in Meetup Location objects, redirect to edit page."""
        url = reverse('approve_meetup_location_request',
                      kwargs={'slug': 'bar'})
        MeetupLocation.objects.create(
            name="Fooo Systers", slug="fooo", location=self.location,
            description="It's a test meetup location", sponsors="BarBaz",
            leader=self.staff_systers_user)
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('meetup/bar/about/'))


class RejectMeetupLocationRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(RejectMeetupLocationRequestViewTestCase, self).setUp()
        self.meetup_location_request = RequestMeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="This is a test meetup location request",
            user=self.systers_user)
        self.staff_user = User.objects.create_superuser(username='foobar', password='foobar',
                                                        email='foobar@test.com')
        self.staff_systers_user = SystersUser.objects.get(user=self.staff_user)

    def test_get_reject_request_meetup_location_view(self):
        url = reverse('reject_meetup_location_request', kwargs={'slug': 'bar'})
        # Test without logging in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Test if accessed by a superuser
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "meetup/confirm_reject_request_meetup_location.html")
        # Test for non existent url
        nonexistent_url = reverse('reject_meetup_location_request',
                                  kwargs={'slug': 'foo'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_post_reject_request_meetup_location_view(self):
        url = reverse('reject_meetup_location_request', kwargs={'slug': 'bar'})
        # Test without logging in
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # Test logging in, normal user
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # Test if superuser posts
        self.client.login(username='foobar', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('view-requests/'))
        # Test non existent url
        nonexistent_url = reverse('reject_meetup_location_request',
                                  kwargs={'slug': 'foo'})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class EditMeetupLocationViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_edit_meetup_location_view(self):
        """Test GET request to edit meetup location"""
        url = reverse("edit_meetup_location", kwargs={'slug': 'foo'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse("edit_meetup_location", kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/edit_meetup_location.html')

    def test_post_edit_meetup_view(self):
        """Test POST request to edit meetup location"""
        url = reverse("edit_meetup_location", kwargs={'slug': 'foo'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse("edit_meetup_location", kwargs={'slug': 'bar'})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        data = {'name': 'Bar Systers', 'slug': 'foo', 'location': self.location.id,
                'description': "It's an edited meetup location", 'sponsors': 'BlackSheep'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/meetup/foo/about/'))


class DeleteMeetupLocationViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(DeleteMeetupLocationViewTestCase, self).setUp()
        self.meetup_location2 = MeetupLocation.objects.create(
            name="Bar Systers", slug="bar", location=self.location,
            description="It's another test meetup location", sponsors="BarBaz",
            leader=self.systers_user)

    def test_get_delete_meetup_location_view(self):
        """Test GET to confirm deletion of meetup location"""
        url = reverse("delete_meetup_location", kwargs={'slug': 'bar'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse("delete_meetup_location", kwargs={'slug': 'baz'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/meetup_location_confirm_delete.html')

    def test_post_delete_meetup_location_view(self):
        """Test POST to delete meetup location"""
        url = reverse("delete_meetup_location", kwargs={'slug': 'bar'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        nonexistent_url = reverse("delete_meetup_location", kwargs={'slug': 'baz'})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/meetup/locations/'))
        self.assertSequenceEqual(MeetupLocation.objects.all(), [self.meetup_location])


class AddMeetupCommentViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_add_meetup_comment_view(self):
        """Test GET request to add a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse('add_meetup_comment', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/add_comment.html')

    def test_post_add_meetup_comment_view(self):
        """Test POST request to add a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse("add_meetup_comment", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        data = {'body': 'This is a test comment'}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].body, 'This is a test comment')
        self.assertEqual(comments[0].author, self.systers_user)
        self.assertEqual(comments[0].content_object, self.meetup)


class EditMeetupCommentViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(EditMeetupCommentViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        meetup_content_type = ContentType.objects.get(app_label='meetup', model='meetup')
        self.comment = Comment.objects.create(author=self.systers_user, is_approved=True,
                                              body='This is a test comment',
                                              content_type=meetup_content_type,
                                              object_id=self.meetup.id)
        # Comment by another user. It should give a 403 Forbidden error.
        self.comment2 = Comment.objects.create(author=self.systers_user2, is_approved=True,
                                               body='This is a test comment',
                                               content_type=meetup_content_type,
                                               object_id=self.meetup.id)

    def test_get_edit_meetup_comment_view(self):
        """Test GET request to edit a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse('edit_meetup_comment', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'comment_pk': self.comment2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_meetup_comment', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'comment_pk': self.comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/edit_comment.html')

    def test_post_edit_meetup_comment_view(self):
        """Test POST request to edit a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse("edit_meetup_comment", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'comment_pk': self.comment.id})
        data = {'body': 'This is an edited test comment'}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 2)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.body, 'This is an edited test comment')
        self.assertEqual(comment.author, self.systers_user)
        self.assertEqual(comment.content_object, self.meetup)


class DeleteMeetupCommentViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(DeleteMeetupCommentViewTestCase, self).setUp()
        self.user2 = User.objects.create_user(username='baz', password='bazbar')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)
        meetup_content_type = ContentType.objects.get(app_label='meetup', model='meetup')
        self.comment = Comment.objects.create(author=self.systers_user, is_approved=True,
                                              body='This is a test comment',
                                              content_type=meetup_content_type,
                                              object_id=self.meetup.id)
        # Comment by another user. It should give a 403 Forbidden error.
        self.comment2 = Comment.objects.create(author=self.systers_user2, is_approved=True,
                                               body='This is a test comment',
                                               content_type=meetup_content_type,
                                               object_id=self.meetup.id)

    def test_get_delete_meetup_comment_view(self):
        """Test GET request to delete a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse('delete_meetup_comment', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'comment_pk': self.comment2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('delete_meetup_comment', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'comment_pk': self.comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_meetup_comment_view(self):
        """Test POST request to delete a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse("delete_meetup_comment", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'comment_pk': self.comment.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)


class RsvpMeetupViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_rsvp_meetup_view(self):
        """Test GET request to rsvp a meetup"""
        url = reverse('rsvp_meetup', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/rsvp_meetup.html')

    def test_post_rsvp_meetup_view(self):
        """Test POST request to rsvp a meetup"""
        url = reverse("rsvp_meetup", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        data = {'coming': True, 'plus_one': False}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        rsvp = Rsvp.objects.all()
        self.assertTrue(len(rsvp), 1)
        self.assertTrue(rsvp[0].user, self.systers_user)
        self.assertTrue(rsvp[0].meetup, self.meetup)


class RsvpGoingViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(RsvpGoingViewTestCase, self).setUp()
        self.rsvp1 = Rsvp.objects.create(user=self.systers_user, meetup=self.meetup,
                                         coming=True, plus_one=False)

    def test_view_rsvp_going_view(self):
        """Test Rsvp going view for correct http response and all Rsvps in a list"""
        self.client.login(username='foo', password='foobar')
        url = reverse("rsvp_going", kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/rsvp_going.html")
        self.assertContains(response, str(self.systers_user))
        self.assertEqual(len(response.context['rsvp_list']), 1)


class AddSupportRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def test_get_add_support_request_view(self):
        """Test GET request to add a new support request"""
        url = reverse('add_support_request', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/add_support_request.html')

    def test_post_add_support_request_view(self):
        """Test POST request to add a new support request"""
        url = reverse('add_support_request', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        data = {'description': 'test support request'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        support_requests = SupportRequest.objects.all()
        self.assertTrue(len(support_requests), 1)
        self.assertTrue(support_requests[0].description, 'test support request')
        self.assertTrue(support_requests[0].volunteer, self.systers_user)
        self.assertTrue(support_requests[0].meetup, self.meetup)


class EditSupportRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(EditSupportRequestViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='This is a test description', is_approved=False)

    def test_get_edit_support_request_view(self):
        """Test GET request to edit a support request for a meetup"""
        url = reverse('edit_support_request', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'pk': self.support_request.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/edit_support_request.html')

    def test_post_edit_support_request_view(self):
        """Test POST request to edit a support request for a meetup"""
        url = reverse('edit_support_request', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'pk': self.support_request.id})
        response = self.client.get(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        data = {'description': 'test support request, edited'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        support_requests = SupportRequest.objects.all()
        self.assertTrue(len(support_requests), 1)
        self.assertTrue(support_requests[0].description, 'test support request')
        self.assertTrue(support_requests[0].volunteer, self.systers_user)
        self.assertTrue(support_requests[0].meetup, self.meetup)


class DeleteSupportRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(DeleteSupportRequestViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='This is a test description', is_approved=False)

    def test_get_delete_support_request_view(self):
        """Test GET to confirm deletion of support request"""
        url = reverse('delete_support_request', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'pk': self.support_request.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_support_request_view(self):
        """Test POST to delete support request"""
        url = reverse('delete_support_request', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'pk': self.support_request.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        support_requests = SupportRequest.objects.all()
        self.assertEqual(len(support_requests), 0)


class SupportRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(SupportRequestViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='This is a test description', is_approved=False)

    def test_view_support_request_view(self):
        """Test Support Request view for correct response"""
        url = reverse('view_support_request', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz',
                      'pk': self.support_request.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/support_request.html')
        self.assertEqual(response.context['meetup'], self.meetup)
        self.assertEqual(response.context['support_request'], self.support_request)


class SupportRequestsListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(SupportRequestsListViewTestCase, self).setUp()
        self.support_request1 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 1', is_approved=True)
        self.support_request2 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 2', is_approved=False)

    def test_view_support_requests_list_view(self):
        """Test Support Requests list view for correct http response and
        all support requests in a list"""
        url = reverse('list_support_requests', kwargs={'slug': 'foo', 'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_support_requests.html")
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 1")


class UnapprovedSupportRequestsListViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(UnapprovedSupportRequestsListViewTestCase, self).setUp()
        self.support_request1 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 1', is_approved=True)
        self.support_request2 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 2', is_approved=False)

    def test_view_unapproved_support_requests_list_view(self):
        """Test unapproved Support Requests list view for correct http response and
        all support requests in a list"""
        url = reverse('unapproved_support_requests', kwargs={'slug': 'foo',
                      'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/unapproved_support_requests.html")
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 2")


class ApproveSupportRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(ApproveSupportRequestViewTestCase, self).setUp()
        self.support_request1 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 1', is_approved=False)
        self.support_request2 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 2', is_approved=False)

    def test_view_approve_support_request_view(self):
        """Test approve support request view for correct http response"""
        url = reverse('approve_support_request', kwargs={'slug': 'foo',
                      'meetup_slug': 'foo-bar-baz', 'pk': self.support_request1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/foo-bar-baz/unapproved_support_requests/')
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 2")


class RejectSupportRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(RejectSupportRequestViewTestCase, self).setUp()
        self.support_request1 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 1', is_approved=False)
        self.support_request2 = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Support Request: 2', is_approved=False)

    def test_view_reject_support_request_view(self):
        """Test reject support request view for correct http response"""
        url = reverse('reject_support_request', kwargs={'slug': 'foo',
                      'meetup_slug': 'foo-bar-baz', 'pk': self.support_request1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo/foo-bar-baz/unapproved_support_requests/')
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 2")


class AddSupportRequestCommentViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(AddSupportRequestCommentViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Test Support Request', is_approved=False)

    def test_get_add_support_request_comment_view(self):
        """Test GET request to add a comment to a support request"""
        url = reverse('add_support_request_comment', kwargs={'slug': 'foo',
                      'meetup_slug': 'foo-bar-baz', 'pk': self.support_request.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/add_comment.html')

    def test_post_add_support_request_comment_view(self):
        """Test POST request to add a support request to a meetup"""
        url = reverse('add_support_request_comment', kwargs={'slug': 'foo',
                      'meetup_slug': 'foo-bar-baz', 'pk': self.support_request.pk})
        response = self.client.get(url, data={})
        self.assertEqual(response.status_code, 403)

        data = {'body': 'This is a test comment'}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].body, 'This is a test comment')
        self.assertEqual(comments[0].author, self.systers_user)
        self.assertEqual(comments[0].content_object, self.support_request)


class EditSupportRequestCommentViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(EditSupportRequestCommentViewTestCase, self).setUp()
        support_request_content_type = ContentType.objects.get(app_label='meetup',
                                                               model='supportrequest')
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Test Support Request', is_approved=False)
        self.comment = Comment.objects.create(author=self.systers_user, is_approved=True,
                                              body='This is a test comment',
                                              content_type=support_request_content_type,
                                              object_id=self.support_request.id)

    def test_get_edit_support_request_comment_view(self):
        """Test GET request to edit a comment to a support request"""
        url = reverse('edit_support_request_comment', kwargs={'slug': 'foo',
                                                              'meetup_slug': 'foo-bar-baz',
                                                              'pk': self.support_request.pk,
                                                              'comment_pk': self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'meetup/edit_comment.html')

    def test_post_edit_support_request_comment_view(self):
        """Test POST request to edit a comment to a support request"""
        url = reverse('edit_support_request_comment', kwargs={'slug': 'foo',
                                                              'meetup_slug': 'foo-bar-baz',
                                                              'pk': self.support_request.pk,
                                                              'comment_pk': self.comment.pk})
        response = self.client.get(url, data={})
        self.assertEqual(response.status_code, 403)

        data = {'body': 'This is an edited test comment'}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].body, 'This is an edited test comment')
        self.assertEqual(comments[0].author, self.systers_user)
        self.assertEqual(comments[0].content_object, self.support_request)


class DeleteSupportRequestCommentViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(DeleteSupportRequestCommentViewTestCase, self).setUp()
        support_request_content_type = ContentType.objects.get(app_label='meetup',
                                                               model='supportrequest')
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Test Support Request', is_approved=False)
        self.comment = Comment.objects.create(author=self.systers_user, is_approved=True,
                                              body='This is a test comment',
                                              content_type=support_request_content_type,
                                              object_id=self.support_request.id)

    def test_get_delete_support_request_comment_view(self):
        """Test GET request to delete a comment to a support request"""
        url = reverse('delete_support_request_comment', kwargs={'slug': 'foo',
                                                                'meetup_slug': 'foo-bar-baz',
                                                                'pk': self.support_request.pk,
                                                                'comment_pk': self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_support_request_comment_view(self):
        """Test POST request to delete a comment to a support request"""
        url = reverse('delete_support_request_comment', kwargs={'slug': 'foo',
                                                                'meetup_slug': 'foo-bar-baz',
                                                                'pk': self.support_request.pk,
                                                                'comment_pk': self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 0)


class CancelMeetupLocationJoinRequestViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        super(CancelMeetupLocationJoinRequestViewTestCase, self).setUp()
        self.password = 'foobar'
        self.meetup_location.members.remove(self.systers_user)

    def test_cancel_meetup_location_join_request(self):
        """Test GET request to cancel a join request to a meetup location"""
        current_url = reverse("about_meetup_location", kwargs={'slug': 'foo'})
        self.data = {
            'current_url': current_url,
            'username': self.user.username
        }
        self.url = reverse("cancel_meetup_location_join_request", kwargs={
            'slug': self.meetup_location.slug,
            'username': self.user.username
        })
        response = self.client.get(self.url, {'current_url': current_url})
        self.assertEqual(response.status_code, 403)

        user = User.objects.create_user(username='bar', password=self.password)
        self.client.login(username=user.username, password=self.password)
        nonexistent_meetup_location_url = reverse("about_meetup_location", kwargs={'slug': 'new'})
        response = self.client.get(nonexistent_meetup_location_url, {
            'current_url': nonexistent_meetup_location_url,
            'username': self.user.username
        })
        self.assertEqual(response.status_code, 404)

        self.check_message_in_response(
            'warning',
            'There is no pending request to join Foo Systers meetup location.',
            200
        )

        self.meetup_location.join_requests.add(self.systers_user)
        self.assertEqual(self.meetup_location.join_requests.all().count(), 1)
        self.check_message_in_response(
            'success',
            'Your request to join Foo Systers meetup location was canceled.',
            200
        )
        self.assertEqual(self.meetup_location.join_requests.all().count(), 0)

        self.meetup_location.members.add(self.systers_user)
        self.check_message_in_response(
            'warning',
            'You are already a member of Foo Systers meetup location. '
            'There is no pending join request.',
            200
        )

    def check_message_in_response(self, _message_tag=None, _message=None, status_code=None):
        response = self.client.get(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, status_code)
        for message in response.context['messages']:
            self.assertEqual(message.tags, _message_tag)
            self.assertTrue(_message in message.message)


class ApiForVmsViewTestCase(APITestCase, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar',
                                             email='user@test.com')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Baz', display_name='Baz', country=country)
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="It's a test meetup location", sponsors="BarBaz", leader=self.systers_user)
        # a meetup after the posted date
        self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                            date='2018-06-16',
                                            time=timezone.now().time(),
                                            description='This is test Meetup',
                                            venue='Foo Systers',
                                            meetup_location=self.meetup_location,
                                            created_by=self.systers_user,
                                            last_updated=timezone.now())
        # a meetup before the posted date
        self.meetup2 = Meetup.objects.create(title='Foo Baz', slug='foobar',
                                             date='2018-06-12',
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             venue='Foo Systers',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())

    def test_api_for_vms_get(self):
        """Test GET request to provide data of all meetups"""
        url = reverse('vms_api')
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         [{u'event_name': u'Foo Baz',
                           u'venue': u'Foo Systers',
                           u'start_date': u'2018-06-12'},
                          {u'event_name': u'Foo Bar Baz',
                           u'venue': u'Foo Systers',
                           u'start_date': u'2018-06-16'}])

    def test_api_for_vms_post(self):
        """Test POST request to provide data of meetups after the specified date"""
        url = reverse('vms_api')
        data = {'date': '2018-06-13'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         [{u'event_name': u'Foo Bar Baz',
                           u'venue': u'Foo Systers',
                           u'start_date': u'2018-06-16'}])


class UpcomingMeetupsSearchViewTestCase(MeetupLocationViewBaseTestCase, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar',
                                             email='user@test.com')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Baz', display_name='Baz', country=country)
        self.location1 = City.objects.all()[0]
        self.meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=self.location,
            description="It's a test meetup location", sponsors="BarBaz", leader=self.systers_user)
        self.meetup_location1 = MeetupLocation.objects.create(
            name="Foo Systers1", slug="foob", location=self.location1,
            description="It's a meetup location", sponsors="BarBaz", leader=self.systers_user)
        self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                            date='2018-06-16',
                                            time=timezone.now().time(),
                                            description='This is test Meetup',
                                            venue='Foo Systers',
                                            meetup_location=self.meetup_location,
                                            created_by=self.systers_user,
                                            last_updated=timezone.now())
        self.meetup2 = Meetup.objects.create(title='Foo Baz', slug='foobar',
                                             date='2018-06-12',
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             venue='Foo Systers',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())
        self.meetup3 = Meetup.objects.create(title='Foob Baz', slug='foobarbaz',
                                             date='2018-06-13',
                                             time=timezone.now().time(),
                                             description='This is test Meetup',
                                             venue='Foo Systers',
                                             meetup_location=self.meetup_location1,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())

    def test_post_view(self):
        """Test post view for all search requests"""
        url = reverse('search_meetups')
        data = {'date': '2018-06-12', 'meeetup_location': 'Foo Systers', 'keyword': 'new'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results':
                         [{'date': '2018-06-12',
                           'meetup': 'Foo Baz',
                           'location': 'Foo Systers',
                           'location_slug': 'foo',
                           'meetup_slug': 'foobar',
                           'distance': '',
                           'unit': ''}]})

        data1 = {'date': '2018-06-13', 'meeetup_location': 'Foo Systers1', 'keyword': 'test',
                 'filter': 2}
        response = self.client.post(url, data1, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results':
                         [{'date': '2018-06-13',
                           'meetup': 'Foob Baz',
                           'location': 'Foo Systers1',
                           'location_slug': 'foob',
                           'meetup_slug': 'foobarbaz',
                           'distance': 2800,
                           'unit': 'kilometers from your location'}]})
