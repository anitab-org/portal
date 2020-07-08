import json
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from django.utils import timezone
from cities_light.models import City, Country
from django.contrib.contenttypes.models import ContentType

from meetup.models import (Meetup, Rsvp, SupportRequest,
                           RequestMeetup)
from users.models import SystersUser
from common.models import Comment


class MeetupBaseCase:
    def setUp(self):
        country = Country.objects.create(name='Bar', continent='AS')
        self.meetup_location = City.objects.create(name='Foo', display_name='Foo',
                                                   country=country)
        self.user = User.objects.create_superuser(username='foo', email="test@gmail.com",
                                                  password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                            date=timezone.now().date(),
                                            time=timezone.now().time(),
                                            description='This is test Meetup',
                                            meetup_location=self.meetup_location,
                                            created_by=self.systers_user,
                                            leader=self.systers_user,
                                            last_updated=timezone.now())


class AllUpcomingMeetupsViewTestCase(MeetupBaseCase, TestCase):
    def test_view_all_upcoming_meetups_list_view(self):
        """Test All Upcoming Meetups list view for correct http response"""
        url = reverse('all_upcoming_meetups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_meetup.html")
        self.assertContains(response, "Foo Bar Baz")
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(len(response.context['meetup_list']), 1)
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             leader=self.systers_user,
                                             last_updated=timezone.now())
        url = reverse('all_upcoming_meetups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_meetup.html")
        self.assertContains(response, "Foo Bar Baz")
        self.assertContains(response, "Bar Baz")
        self.assertEqual(len(response.context['object_list']), 2)
        self.assertEqual(len(response.context['meetup_list']), 2)


class MeetupViewTestCase(MeetupBaseCase, TestCase):
    def test_view_meetup(self):
        """Test Meetup view for correct response"""
        url = reverse('view_meetup', kwargs={'slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/meetup.html')
        self.assertEqual(response.context['meetup'], self.meetup)

        nonexistent_url = reverse('view_meetup', kwargs={'slug': 'bazbar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class AddMeetupViewTestCase(MeetupBaseCase, TestCase):
    def test_get_add_meetup_view(self):
        """Test GET request to add a new meetup"""
        url = reverse('add_meetup')
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
        url = reverse("add_meetup")
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        date = (timezone.now() + timezone.timedelta(2)).date()
        time = timezone.now().time()
        data = {'title': 'BarTest', 'slug': 'bartest', 'date': date, 'time': time,
                'meetup_location': self.meetup_location.id,
                'description': "It's a test meetup."}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        new_meetup = Meetup.objects.get(slug='bartest')
        self.assertTrue(new_meetup.title, 'BarTest')
        self.assertTrue(new_meetup.created_by, self.systers_user)
        self.assertTrue(new_meetup.meetup_location, self.meetup_location)


class RequestMeetupViewTestCase(MeetupBaseCase, TestCase):
    def test_get_request_meetup_view(self):
        """Test GET request to request a new meetup"""
        url = reverse('request_meetup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/request_new_meetup.html')

    def test_post_request_meetup_view(self):
        """Test POST request to request a new meetup"""
        url = reverse("request_meetup")
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        date = (timezone.now() + timezone.timedelta(2)).date()
        time = timezone.now().time()
        data = {'title': 'BarTest', 'slug': 'bartest', 'date': date, 'time': time,
                'meetup_location': self.meetup_location.id,
                'description': "It's a test meetup."}
        response = self.client.post(url, data=data, created_by=self.systers_user)
        self.assertEqual(response.status_code, 302)
        new_meetup_request = RequestMeetup.objects.get(slug='bartest')
        self.assertTrue(new_meetup_request.title, 'BarTest')
        self.assertTrue(new_meetup_request.created_by, self.systers_user)
        self.assertTrue(new_meetup_request.meetup_location, self.meetup_location)


class NewMeetupRequestsListViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(NewMeetupRequestsListViewTestCase, self).setUp()
        self.meetup_request1 = RequestMeetup.objects.create(
            title="Bar Talk", slug="bar", date=timezone.now().date(),
            time=timezone.now().time(),
            description="This is a test meetup meetup_location request1",
            created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.meetup_request2 = RequestMeetup.objects.create(
            title="Foo Talk", slug="foo", date=timezone.now().date(),
            time=timezone.now().time(),
            description="This is a test meetup meetup_location request2",
            created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_view_new_meetup_meetup_location_requests_list_view(self):
        """Test Meetup Requests list view for correct http response and
        all meetup requests in a list"""
        url = reverse('new_meetup_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Testing after logggin in - normal user
        self.client.login(username='foobar', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Testing after logging in - Organizer of the Meetup meetup_location
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "meetup/new_meetup_requests.html")
        self.assertContains(response, "Foo Talk")
        self.assertSequenceEqual(RequestMeetup.objects.filter(
            is_approved=False), [self.meetup_request1, self.meetup_request2])
        self.assertContains(response, "Requested by")


class ViewMeetupRequestViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(ViewMeetupRequestViewTestCase, self).setUp()
        self.meetup_request = RequestMeetup.objects.create(
            title="Foo Talk", slug="bar", date=timezone.now().date(),
            time=timezone.now().time(),
            description="This is a test meetup meetup_location request",
            created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_view_meetup_request_view(self):
        """Test Meetup Request view for correct response"""
        # Test without logging in
        url = reverse('view_meetup_request', kwargs={'meetup_slug': 'bar'})
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


class ApproveRequestMeetupViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(ApproveRequestMeetupViewTestCase, self).setUp()
        self.meetup_request = RequestMeetup.objects.create(
            title="Foo Talk", slug="bar", date=timezone.now().date(),
            time=timezone.now().time(),
            description="This is a test meetup meetup_location request",
            created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_approve_request_meetup_view_base(self):
        url = reverse('approve_meetup_request',
                      kwargs={'meetup_slug': 'bar'})
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
        self.assertTrue(response.url.endswith('meetup/bar/'))
        # Test for non existent url
        nonexistent_url = reverse('approve_meetup_request',
                                  kwargs={'meetup_slug': 'carr'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_approve_request_meetup_view_slug(self):
        """Test if slug already exists in Meetup meetup_location objects, redirect to edit page."""
        url = reverse('approve_meetup_request',
                      kwargs={'meetup_slug': 'bar'})
        Meetup.objects.create(title='Foo Bar Baz', slug='bar',
                              date=timezone.now().date(),
                              time=timezone.now().time(),
                              description='This is test Meetup',
                              meetup_location=self.meetup_location,
                              created_by=self.systers_user,
                              leader=self.systers_user,
                              last_updated=timezone.now())
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('meetup/view_meetup_requests/'))


class RejectMeetupRequestViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(RejectMeetupRequestViewTestCase, self).setUp()
        self.meetup_request = RequestMeetup.objects.create(
            title="Foo Talk", slug="bar", date=timezone.now().date(),
            time=timezone.now().time(),
            description="This is a test meetup request",
            created_by=self.systers_user,
            meetup_location=self.meetup_location)
        self.password = 'foobar'
        self.user2 = User.objects.create(username='foobar', password=self.password,
                                         email='foo@test.com')
        self.systers_user2 = SystersUser.objects.get(user=self.user2)

    def test_get_reject_request_meetup_view(self):
        url = reverse('reject_meetup_request', kwargs={'meetup_slug': 'bar'})
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
                                  kwargs={'meetup_slug': 'barr'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_post_reject_request_meetup_meetup_location_view(self):
        url = reverse('reject_meetup_request', kwargs={'meetup_slug': 'bar'})
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
                                  kwargs={'meetup_slug': 'barr'})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class DeleteMeetupViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(DeleteMeetupViewTestCase, self).setUp()
        self.meetup2 = Meetup.objects.create(title='Fooba', slug='fooba',
                                             date=timezone.now().date(),
                                             time=timezone.now().time(),
                                             description='This is test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             leader=self.systers_user,
                                             last_updated=timezone.now())
        self.client = Client()

    def test_get_delete_meetup_view(self):
        """Test GET to confirm deletion of meetup"""
        url = reverse("delete_meetup", kwargs={'meetup_slug': 'fooba'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_meetup_view(self):
        """Test POST to delete a meetup"""
        url = reverse("delete_meetup", kwargs={'meetup_slug': 'fooba'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # One meetup deleted, another meetup left initialized in
        # Meetupmeetup_locationViewBaseTestCase
        self.assertSequenceEqual(Meetup.objects.all(), [self.meetup])


class EditMeetupView(MeetupBaseCase, TestCase):
    def test_get_edit_meetup_view(self):
        """Test GET edit meetup"""
        wrong_url = reverse("edit_meetup", kwargs={'meetup_slug': 'foo'})
        response = self.client.get(wrong_url)
        self.assertEqual(response.status_code, 403)

        url = reverse("edit_meetup", kwargs={'meetup_slug': 'foo-bar-baz'})
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
        wrong_url = reverse("edit_meetup", kwargs={'meetup_slug': 'foo'})
        response = self.client.post(wrong_url)
        self.assertEqual(response.status_code, 403)

        url = reverse("edit_meetup", kwargs={'meetup_slug': 'foo-bar-baz'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        date = (timezone.now() + timezone.timedelta(2)).date()
        time = timezone.now().time()
        data = {'title': 'BarTes', 'slug': 'bartes', 'date': date, 'time': time,
                'meetup_location': self.meetup_location,
                'description': "It's a edit test meetup."}
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/meetup/bartes/'))


class UpcomingMeetupsViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(UpcomingMeetupsViewTestCase, self).setUp()
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             leader=self.systers_user,
                                             last_updated=timezone.now())

    def test_view_upcoming_meetup_list_view(self):
        """Test Upcoming Meetup list view for correct http response and
        all upcoming meetups in a list"""
        url = reverse('upcoming_meetups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/upcoming_meetups.html")
        self.assertContains(response, "Foo Bar Baz")
        self.assertContains(response, "Bar Baz")
        self.assertEqual(len(response.context['meetup_list']), 2)


class PastMeetupListViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(PastMeetupListViewTestCase, self).setUp()
        # a future meetup. This should not show up under 'past meetups'.
        self.meetup2 = Meetup.objects.create(title='Bar Baz', slug='bazbar',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             leader=self.systers_user,
                                             last_updated=timezone.now())
        # a past meetup. This should show up under 'past meetups'.
        self.meetup3 = Meetup.objects.create(title='Foo Baz', slug='foobar',
                                             date=(timezone.now() - timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             meetup_location=self.meetup_location,
                                             created_by=self.systers_user,
                                             leader=self.systers_user,
                                             last_updated=timezone.now())

    def test_view_past_meetup_list_view(self):
        """Test Past Meetup list view for correct http response and
        all past meetups in a list"""
        url = reverse('past_meetups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/past_meetups.html")
        self.assertEqual(len(response.context['meetup_list']), 1)


class AddMeetupCommentViewTestCase(MeetupBaseCase, TestCase):
    def test_get_add_meetup_comment_view(self):
        """Test GET request to add a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse('add_meetup_comment', kwargs={'meetup_slug': 'foo-bar-baz'})
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
        url = reverse("add_meetup_comment", kwargs={'meetup_slug': 'foo-bar-baz'})
        data = {'body': 'This is a test comment'}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].body, 'This is a test comment')
        self.assertEqual(comments[0].author, self.systers_user)
        self.assertEqual(comments[0].content_object, self.meetup)


class EditMeetupCommentViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('edit_meetup_comment', kwargs={'meetup_slug': 'foo-bar-baz',
                                                     'comment_pk': self.comment2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('edit_meetup_comment', kwargs={'meetup_slug': 'foo-bar-baz',
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
        url = reverse("edit_meetup_comment", kwargs={'meetup_slug': 'foo-bar-baz',
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


class DeleteMeetupCommentViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('delete_meetup_comment', kwargs={'meetup_slug': 'foo-bar-baz',
                                                       'comment_pk': self.comment2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        url = reverse('delete_meetup_comment', kwargs={'meetup_slug': 'foo-bar-baz',
                                                       'comment_pk': self.comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_meetup_comment_view(self):
        """Test POST request to delete a comment to a meetup"""
        self.client.login(username='foo', password='foobar')
        url = reverse("delete_meetup_comment", kwargs={'meetup_slug': 'foo-bar-baz',
                                                       'comment_pk': self.comment.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)


class RsvpMeetupViewTestCase(MeetupBaseCase, TestCase):
    def test_get_rsvp_meetup_view(self):
        """Test GET request to rsvp a meetup"""
        url = reverse('rsvp_meetup', kwargs={'meetup_slug': 'foo-bar-baz'})
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
        url = reverse("rsvp_meetup", kwargs={'meetup_slug': 'foo-bar-baz'})
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


class RsvpGoingViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(RsvpGoingViewTestCase, self).setUp()
        self.rsvp1 = Rsvp.objects.create(user=self.systers_user, meetup=self.meetup,
                                         coming=True, plus_one=False)

    def test_view_rsvp_going_view(self):
        """Test Rsvp going view for correct http response and all Rsvps in a list"""
        self.client.login(username='foo', password='foobar')
        url = reverse("rsvp_going", kwargs={'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/rsvp_going.html")
        self.assertContains(response, str(self.systers_user))
        self.assertEqual(len(response.context['rsvp_list']), 1)


class AddSupportRequestViewTestCase(MeetupBaseCase, TestCase):
    def test_get_add_support_request_view(self):
        """Test GET request to add a new support request"""
        url = reverse('add_support_request', kwargs={'meetup_slug': 'foo-bar-baz'})
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
        url = reverse('add_support_request', kwargs={'meetup_slug': 'foo-bar-baz'})
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


class EditSupportRequestViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(EditSupportRequestViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='This is a test description', is_approved=False)

    def test_get_edit_support_request_view(self):
        """Test GET request to edit a support request for a meetup"""
        url = reverse('edit_support_request', kwargs={'meetup_slug': 'foo-bar-baz',
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
        url = reverse('edit_support_request', kwargs={'meetup_slug': 'foo-bar-baz',
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


class DeleteSupportRequestViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(DeleteSupportRequestViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='This is a test description', is_approved=False)

    def test_get_delete_support_request_view(self):
        """Test GET to confirm deletion of support request"""
        url = reverse('delete_support_request', kwargs={'meetup_slug': 'foo-bar-baz',
                                                        'pk': self.support_request.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_support_request_view(self):
        """Test POST to delete support request"""
        url = reverse('delete_support_request', kwargs={'meetup_slug': 'foo-bar-baz',
                                                        'pk': self.support_request.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        support_requests = SupportRequest.objects.all()
        self.assertEqual(len(support_requests), 0)


class SupportRequestViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(SupportRequestViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='This is a test description', is_approved=False)

    def test_view_support_request_view(self):
        """Test Support Request view for correct response"""
        url = reverse('view_support_request', kwargs={'meetup_slug': 'foo-bar-baz',
                                                      'pk': self.support_request.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetup/support_request.html')
        self.assertEqual(response.context['meetup'], self.meetup)
        self.assertEqual(response.context['support_request'], self.support_request)


class SupportRequestsListViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('list_support_requests', kwargs={'meetup_slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/list_support_requests.html")
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 1")


class UnapprovedSupportRequestsListViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('unapproved_support_requests', kwargs={'slug': 'foo-bar-baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetup/unapproved_support_requests.html")
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 2")


class ApproveSupportRequestViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('approve_support_request',
                      kwargs={'meetup_slug': 'foo-bar-baz',
                              'pk': self.support_request1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo-bar-baz/unapproved_support_requests/')
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 2")


class RejectSupportRequestViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('reject_support_request',
                      kwargs={'meetup_slug': 'foo-bar-baz',
                              'pk': self.support_request1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/meetup/foo-bar-baz/unapproved_support_requests/')
        self.assertEqual(len(response.context['supportrequest_list']), 1)
        self.assertEqual(response.context['supportrequest_list'][0].description,
                         "Support Request: 2")


class AddSupportRequestCommentViewTestCase(MeetupBaseCase, TestCase):
    def setUp(self):
        super(AddSupportRequestCommentViewTestCase, self).setUp()
        self.support_request = SupportRequest.objects.create(
            volunteer=self.systers_user, meetup=self.meetup,
            description='Test Support Request', is_approved=False)

    def test_get_add_support_request_comment_view(self):
        """Test GET request to add a comment to a support request"""
        url = reverse('add_support_request_comment', kwargs={'meetup_slug': 'foo-bar-baz',
                                                             'pk': self.support_request.pk})
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
        url = reverse('add_support_request_comment', kwargs={'meetup_slug': 'foo-bar-baz',
                                                             'pk': self.support_request.pk})
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


class EditSupportRequestCommentViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('edit_support_request_comment', kwargs={'meetup_slug': 'foo-bar-baz',
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
        url = reverse('edit_support_request_comment', kwargs={'meetup_slug': 'foo-bar-baz',
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


class DeleteSupportRequestCommentViewTestCase(MeetupBaseCase, TestCase):
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
        url = reverse('delete_support_request_comment', kwargs={'meetup_slug': 'foo-bar-baz',
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
        url = reverse('delete_support_request_comment', kwargs={'meetup_slug': 'foo-bar-baz',
                                                                'pk': self.support_request.pk,
                                                                'comment_pk': self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 0)


# class ApiForVmsViewTestCase(APITestCase, TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='foo', password='foobar',
#                                              email='user@test.com')
#         self.systers_user = SystersUser.objects.get(user=self.user)
#         country = Country.objects.create(name='Bar', continent='AS')
#         self.meetup_location = City.objects.create(name='Baz', display_name='Baz',
#         country=country)
#         # a meetup after the posted date
#         self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
#                                             date='2018-06-16',
#                                             time=timezone.now().time(),
#                                             description='This is test Meetup',
#                                             venue='Foo Systers',
#                                             meetup_location=self.meetup_location,
#                                             created_by=self.systers_user,
#                                             last_updated=timezone.now(),
#                                             leader=self.systers_user,
#                                             end_date='2018-12-16')
#         # a meetup before the posted date
#         self.meetup2 = Meetup.objects.create(title='Foo Baz', slug='foobar',
#                                              date='2018-06-12',
#                                              time=timezone.now().time(),
#                                              description='This is new test Meetup',
#                                              venue='Foo Systers',
#                                              meetup_location=self.meetup_location,
#                                              created_by=self.systers_user,
#                                              leader=self.systers_user,
#                                              last_updated=timezone.now(),
#                                              end_date='2018-12-16')
#
#     def test_api_for_vms_get(self):
#         """Test GET request to provide data of all meetups"""
#         url = reverse('vms_api')
#         response = self.client.get(url)
#         self.assertEqual(json.loads(response.content.decode('utf-8')),
#                          [{u'event_name': u'Foo Baz',
#                            u'venue': u'Foo Systers',
#                            u'start_date': u'2018-06-12',
#                            u'end_date': u'2018-12-16',
#                            u'meetup_id': 33,
#                            u'description': u'This is new test Meetup'},
#                           {u'event_name': u'Foo Bar Baz',
#                            u'venue': u'Foo Systers',
#                            u'start_date': u'2018-06-16',
#                            u'end_date': u'2018-12-16',
#                            u'meetup_id': 32,
#                            u'description': u'This is test Meetup'}])
#
#     def test_api_for_vms_post(self):
#         """Test POST request to provide data of meetups after the specified date"""
#         url = reverse('vms_api')
#         data = {'meetup_id': 38}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(json.loads(response.content.decode('utf-8')),
#                          [{u'event_name': u'Foo Baz',
#                            u'venue': u'Foo Systers',
#                            u'start_date': u'2018-06-12',
#                            u'end_date': u'2018-12-16',
#                            u'meetup_id': 41,
#                            u'description': u'This is new test Meetup'},
#                           {u'event_name': u'Foo Bar Baz',
#                            u'venue': u'Foo Systers',
#                            u'start_date': u'2018-06-16',
#                            u'end_date': u'2018-12-16',
#                            u'meetup_id': 40,
#                            u'description': u'This is test Meetup'}])


class UpcomingMeetupsSearchViewTestCase(MeetupBaseCase, TestCase):
    maxDiff = None

    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar',
                                             email='user@test.com')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Baz', display_name='Baz', country=country)
        self.meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                            date=(timezone.now() + timezone.timedelta(4)).date(),
                                            time=timezone.now().time(),
                                            description='This is test Meetup',
                                            venue='Foo Systers',
                                            meetup_location=self.location,
                                            created_by=self.systers_user,
                                            leader=self.systers_user,
                                            last_updated=timezone.now())

        self.meetup2 = Meetup.objects.create(title='Foo Baz', slug='foobar',
                                             date=timezone.now().date(),
                                             time=timezone.now().time(),
                                             description='This is new test Meetup',
                                             venue='Foo Systers',
                                             meetup_location=self.location,
                                             created_by=self.systers_user,
                                             leader=self.systers_user,
                                             last_updated=timezone.now())

        self.meetup3 = Meetup.objects.create(title='Foob Baz', slug='foobarbaz',
                                             date=(timezone.now() + timezone.timedelta(2)).date(),
                                             time=timezone.now().time(),
                                             description='This is test Meetup',
                                             venue='Foo Systers',
                                             meetup_location=self.location,
                                             leader=self.systers_user,
                                             created_by=self.systers_user,
                                             last_updated=timezone.now())

    def test_post_view(self):
        """Test post view for all search requests"""
        url = reverse('search_meetups')
        data = {'keyword': 'Foo Baz'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results': [{'date': self.meetup2.date.isoformat(),
                                              'meetup': 'Foo Baz',
                                              'location': 'Baz',
                                              'meetup_slug': 'foobar',
                                              'distance': 900}],
                          'unit': 'kilometers from your location'})

        data1 = {'keyword': 'Foo Bar'}
        response = self.client.post(url, data1, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results': [{'date': self.meetup.date.isoformat(),
                                              'meetup': 'Foo Bar Baz',
                                              'location': 'Baz',
                                              'meetup_slug': 'foo-bar-baz',
                                              'distance': 900}],
                          'unit': 'kilometers from your location'})

        data2 = {'keyword': 'Foo Bar', 'location': 'Baz'}
        response = self.client.post(url, data2, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results': [{'date': self.meetup.date.isoformat(),
                                              'meetup': 'Foo Bar Baz',
                                              'location': 'Baz',
                                              'meetup_slug': 'foo-bar-baz',
                                              'distance': 0}],
                          'unit': 'kilometers from your location'})

        data3 = {'keyword': 'new'}
        response = self.client.post(url, data3, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results': [],
                          'unit': ''})

        data4 = {'keyword': 'Foob'}
        response = self.client.post(url, data4, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results': [{'date': self.meetup3.date.isoformat(),
                                              'meetup': 'Foob Baz',
                                              'location': 'Baz',
                                              'meetup_slug': 'foobarbaz',
                                              'distance': 900}],
                          'unit': 'kilometers from your location'})

        data5 = {'keyword': 'Foo', 'location': 'Baz'}
        response = self.client.post(url, data5, format='json')
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'search_results': [{'date': self.meetup2.date.isoformat(),
                                              'meetup': 'Foo Baz',
                                              'location': 'Baz',
                                              'meetup_slug': 'foobar',
                                              'distance': 0},
                                             {'date': self.meetup3.date.isoformat(),
                                              'meetup': 'Foob Baz',
                                              'location': 'Baz',
                                              'meetup_slug': 'foobarbaz',
                                              'distance': 0},
                                             {'date': self.meetup.date.isoformat(),
                                              'meetup': 'Foo Bar Baz',
                                              'location': 'Baz',
                                              'meetup_slug': 'foo-bar-baz',
                                              'distance': 0},
                                             ],
                          'unit': 'kilometers from your location'})
