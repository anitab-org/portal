from django.contrib.auth.models import User, Group
from django.test import TestCase

from community.models import Community, JoinRequest
from users.models import SystersUser


class SystersUserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()

    def test_create_systers_user(self):
        """Test creation of SystersUser on new User create"""
        self.assertTrue(1, SystersUser.objects.count())
        self.assertEqual(self.systers_user.user,
                         SystersUser.objects.get().user)

        self.systers_user.user.save()
        self.assertTrue(1, SystersUser.objects.count())

    def test_join_group(self):
        """Test SystersUser joining an auth Group"""
        group = Group.objects.create(name="Baz")
        self.assertSequenceEqual(self.systers_user.user.groups.all(), [])
        self.systers_user.join_group(group)
        self.assertEqual(self.systers_user.user.groups.get(), group)

    def test_leave_group(self):
        """Test SystersUser leaving an auth Group"""
        group = Group.objects.create(name="Baz")
        self.systers_user.leave_group(group)
        self.systers_user.join_group(group)
        self.assertEqual(self.systers_user.user.groups.get(), group)
        self.systers_user.leave_group(group)
        self.assertSequenceEqual(self.systers_user.user.groups.all(), [])

    def test_is_member(self):
        """Test if SystersUser is a member of a Community"""
        community = Community.objects.create(name="Foo", slug="foo",
                                             order=1,
                                             community_admin=self.systers_user)
        user = User.objects.create_user(username='bar', password='foobar')
        bar_systers_user = SystersUser.objects.get(user=user)
        self.assertFalse(bar_systers_user.is_member(community))
        community.add_member(bar_systers_user)
        community.save()
        self.assertTrue(bar_systers_user.is_member(community))

    def test_get_last_join_request(self):
        """Test fetching last join request made to a community"""
        community = Community.objects.create(name="Foo", slug="foo",
                                             order=1,
                                             community_admin=self.systers_user)
        user = User.objects.create_user(username='bar', password='foobar')
        bar_systers_user = SystersUser.objects.get(user=user)
        self.assertIsNone(bar_systers_user.get_last_join_request(community))
        join_request1 = JoinRequest.objects.create(user=bar_systers_user,
                                                   community=community)
        self.assertEqual(bar_systers_user.get_last_join_request(community),
                         join_request1)
        join_request2 = JoinRequest.objects.create(user=bar_systers_user,
                                                   community=community)
        self.assertEqual(bar_systers_user.get_last_join_request(community),
                         join_request2)

    def test_approve_all_join_requests(self):
        """Test approving all user join requests"""
        community = Community.objects.create(name="Foo", slug="foo",
                                             order=1,
                                             community_admin=self.systers_user)
        user = User.objects.create_user(username='bar', password='foobar')
        bar_systers_user = SystersUser.objects.get(user=user)
        status = bar_systers_user.approve_all_join_requests(community)
        self.assertEqual(status, "no_pending_join_request")
        join_request1 = JoinRequest.objects.create(user=bar_systers_user,
                                                   community=community)
        join_request2 = JoinRequest.objects.create(user=bar_systers_user,
                                                   community=community)
        self.assertFalse(join_request1.is_approved)
        self.assertFalse(join_request2.is_approved)

        status = bar_systers_user.approve_all_join_requests(community)
        self.assertEqual(status, "ok")
        join_requests = JoinRequest.objects.all()
        for join_request in join_requests:
            self.assertTrue(join_request.is_approved)

    def test_reject_all_join_requests(self):
        """Test rejecting all user join requests"""
        community = Community.objects.create(name="Foo", slug="foo",
                                             order=1,
                                             community_admin=self.systers_user)
        user = User.objects.create_user(username='bar', password='foobar')
        bar_systers_user = SystersUser.objects.get(user=user)
        status = bar_systers_user.delete_all_join_requests(community)
        self.assertEqual(status, "no_pending_join_request")

        JoinRequest.objects.create(user=bar_systers_user, community=community)
        JoinRequest.objects.create(user=bar_systers_user, community=community)
        status = bar_systers_user.delete_all_join_requests(community)
        self.assertEqual(status, "ok")
        self.assertFalse(bar_systers_user.is_member(community))
        self.assertSequenceEqual(JoinRequest.objects.all(), [])


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')

    def test_unicode(self):
        """Test unicode representation of Django User model"""
        self.assertEqual(unicode(self.user), 'foo')
        self.user.first_name = "Foo"
        self.user.save()
        self.assertEqual(unicode(self.user), 'foo')
        self.user.last_name = "Bar"
        self.user.save()
        self.assertEqual(unicode(self.user), 'Foo Bar')
