from cities_light.models import Country, City
from django.contrib.auth.models import User, Group
from django.test import TestCase

from community.models import Community
from community.utils import create_groups
from community.permissions import groups_templates
from membership.models import JoinRequest
from users.models import SystersUser


class SystersUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)

    def test_create_systers_user(self):
        """Test creation of SystersUser on new User create"""
        self.assertTrue(1, SystersUser.objects.count())
        self.assertEqual(self.systers_user.user,
                         SystersUser.objects.get(user=self.user).user)

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

    def test_leave_groups(self):
        """Test SystersUser leaving all Community groups"""
        name = "Baz"
        self.systers_user.leave_groups(name)
        self.assertSequenceEqual(self.systers_user.user.groups.all(), [])
        create_groups(name, groups_templates)
        content_manager_group = Group.objects.get(name="Baz: Content Manager")
        self.systers_user.join_group(content_manager_group)
        self.assertSequenceEqual(self.systers_user.user.groups.all(),
                                 [content_manager_group])
        self.systers_user.leave_groups(name)
        self.assertSequenceEqual(self.systers_user.user.groups.all(), [])
        other_name = "Foo"
        create_groups(other_name, groups_templates)
        admin_group = Group.objects.get(name="Foo: Community Admin")
        self.systers_user.join_group(admin_group)
        self.systers_user.join_group(content_manager_group)
        self.assertCountEqual(list(self.systers_user.user.groups.all()),
                              [content_manager_group, admin_group])
        self.systers_user.leave_groups(name)
        self.assertSequenceEqual(self.systers_user.user.groups.all(),
                                 [admin_group])

    def test_is_member(self):
        """Test if SystersUser is a member of a Community"""
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        community = Community.objects.create(name="Foo", slug="foo",
                                             order=1, location=location,
                                             admin=self.systers_user)
        user = User.objects.create_user(username='bar', password='foobar')
        bar_systers_user = SystersUser.objects.get(user=user)
        self.assertFalse(bar_systers_user.is_member(community))
        community.add_member(bar_systers_user)
        community.save()
        self.assertTrue(bar_systers_user.is_member(community))

    def test_is_group_member(self):
        """Test if SystersUser is a member of a group"""
        group = Group.objects.create(name="Foo")
        self.assertFalse(self.systers_user.is_group_member("Foo"))
        self.systers_user.join_group(group)
        self.assertTrue(self.systers_user.is_group_member("Foo"))

    def test_get_member_groups(self):
        """Test getting groups of which the user is a member"""
        groups = create_groups("Bar", groups_templates)
        self.assertEqual(self.systers_user.get_member_groups(groups), [])
        first_group = groups[0]
        self.systers_user.join_group(first_group)
        self.assertSequenceEqual(self.systers_user.get_member_groups(groups),
                                 [first_group])
        last_group = groups[-1]
        self.systers_user.join_group(last_group)
        self.assertCountEqual(self.systers_user.get_member_groups(groups),
                              [first_group, last_group])
        group = Group.objects.create(name="Dummy")
        self.systers_user.join_group(group)
        self.assertCountEqual(self.systers_user.get_member_groups(groups),
                              [first_group, last_group])

    def test_get_last_join_request(self):
        """Test fetching last join request made to a community"""
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

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
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        community = Community.objects.create(name="Foo", slug="foo",
                                             order=1, location=location,
                                             admin=self.systers_user)
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
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)
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

    def test_leave_community(self):
        """Test leaving a community"""
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        community = Community.objects.create(name="Foo", slug="foo",
                                             order=1, location=location,
                                             admin=self.systers_user)
        status = self.systers_user.leave_community(community)
        self.assertEqual(status, "is_admin")

        user = User.objects.create_user(username='bar', password='foobar')
        bar_systers_user = SystersUser.objects.get(user=user)
        status = bar_systers_user.leave_community(community)
        self.assertEqual(status, "not_member")

        community.add_member(bar_systers_user)
        community.save()
        self.assertTrue(bar_systers_user.is_member(community))
        status = bar_systers_user.leave_community(community)
        self.assertEqual(status, "ok")
        self.assertFalse(bar_systers_user.is_member(community))

        community.add_member(bar_systers_user)
        community.save()
        self.assertTrue(bar_systers_user.is_member(community))
        content_manager_group = Group.objects.get(name="Foo: Content Manager")
        bar_systers_user.join_group(content_manager_group)
        self.assertSequenceEqual(bar_systers_user.user.groups.all(),
                                 [content_manager_group])
        status = bar_systers_user.leave_community(community)
        self.assertEqual(status, "ok")
        self.assertFalse(bar_systers_user.is_member(community))
        self.assertSequenceEqual(bar_systers_user.user.groups.all(), [])


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')

    def test_str(self):
        """Test string representation of Django User model"""
        self.assertEqual(str(self.user), 'foo')
        self.user.first_name = "Foo"
        self.user.save()
        self.assertEqual(str(self.user), 'foo')
        self.user.last_name = "Bar"
        self.user.save()
        self.assertEqual(str(self.user), 'Foo Bar')
