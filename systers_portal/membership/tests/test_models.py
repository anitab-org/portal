from cities_light.models import Country, City
from django.test import TestCase
from django.contrib.auth.models import User

from community.models import Community
from membership.models import JoinRequest
from users.models import SystersUser


class JoinRequestModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_unicode(self):
        """Test JoinRequest object string representation"""
        join_request = JoinRequest(user=self.systers_user,
                                   community=self.community)
        self.assertEqual(str(join_request),
                         "Join Request by foo - not approved")
        join_request.is_approved = True
        join_request.save()
        self.assertEqual(str(join_request),
                         "Join Request by foo - approved")

    def test_approve(self):
        """Test approving a join request"""
        join_request = JoinRequest(user=self.systers_user,
                                   community=self.community)
        self.assertFalse(join_request.is_approved)
        join_request.approve()
        self.assertTrue(join_request.is_approved)
        join_request.approve()
        self.assertTrue(join_request.is_approved)

    def test_create_join_request(self):
        """Test model manager method to create a join request"""
        user = User.objects.create(username="bar", password="foobar")
        systers_user = SystersUser.objects.get(user=user)
        join_request, status = JoinRequest.objects.create_join_request(
            systers_user, self.community)
        self.assertEqual(join_request, JoinRequest.objects.get())
        self.assertEqual(status, "ok")

        join_request, status = JoinRequest.objects.create_join_request(
            systers_user, self.community)
        self.assertIsNone(join_request)
        self.assertEqual(status, "join_request_exists")

        join_request = JoinRequest.objects.get()
        join_request.approve()
        self.community.add_member(systers_user)
        join_request, status = JoinRequest.objects.create_join_request(
            systers_user, self.community)
        self.assertIsNone(join_request)
        self.assertEqual(status, "already_member")

        self.community.remove_member(systers_user)
        join_request, status = JoinRequest.objects.create_join_request(
            systers_user, self.community)
        self.assertIsInstance(join_request, JoinRequest)
        self.assertEqual(status, "ok")

    def test_cancel_join_request(self):
        """Test model manager method to cancel join requests"""
        user = User.objects.create(username="bar", password="foobar")
        systers_user = SystersUser.objects.get(user=user)

        status = JoinRequest.objects.cancel_join_request(systers_user,
                                                         self.community)
        self.assertEqual(status, "no_pending_join_request")

        JoinRequest.objects.create(user=systers_user, community=self.community)
        status = JoinRequest.objects.cancel_join_request(systers_user,
                                                         self.community)
        self.assertEqual(status, "ok")
        self.assertSequenceEqual(JoinRequest.objects.all(), [])

        self.community.add_member(systers_user)
        self.community.save()

        status = JoinRequest.objects.cancel_join_request(systers_user,
                                                         self.community)
        self.assertEqual(status, "already_member")

        JoinRequest.objects.create(user=systers_user, community=self.community)
        status = JoinRequest.objects.cancel_join_request(systers_user,
                                                         self.community)
        self.assertEqual(status, "already_member")
