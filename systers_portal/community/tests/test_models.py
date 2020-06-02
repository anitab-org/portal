from cities_light.models import City, Country
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_delete
from django.test import TestCase

from community.constants import COMMUNITY_ADMIN
from community.models import Community, CommunityPage, RequestCommunity
from community.signals import (manage_community_groups, remove_community_groups)
from users.models import SystersUser


class RequestCommunityModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.request_community = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, is_member='Yes', type_community='Other',
            location=location, community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_str(self):
        """Test RequestCommunity object string representation"""
        self.assertEqual(str(self.request_community), "Foo")

    def test_get_fields(self):
        """Test getting RequestCommunity fields"""
        fields = self.request_community.get_fields()
        self.assertTrue(len(fields), 28)
        self.assertTrue(fields[1], ('name', 'Foo'))

    def test_get_verbose_fields(self):
        """Test getting RequestCommunity verbose fields"""
        fields = self.request_community.get_fields()
        self.assertTrue(len(fields), 28)
        self.assertTrue(fields[1], ('Proposed Community Name', 'Foo'))


class CommunityModelTestCase(TestCase):
    def setUp(self):
        post_save.disconnect(manage_community_groups, sender=Community,
                             dispatch_uid="manage_groups")
        post_delete.disconnect(remove_community_groups, sender=Community,
                               dispatch_uid="remove_groups")
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        self.location = City.objects.create(name='Foo', display_name='Foo',
                                            country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=self.location,
                                                  admin=self.systers_user)

    def test_str(self):
        """Test Community object string representation"""
        self.assertEqual(str(self.community), "Foo")

    def test_original_values(self):
        """Test original community name and admin functioning"""
        self.assertEqual(self.community.original_name, "Foo")
        self.assertEqual(self.community.admin, self.systers_user)
        self.community.name = "Bar"
        user = User.objects.create(username="bar", password="barfoo")
        systers_user2 = SystersUser.objects.get(user=user)
        self.community.admin = systers_user2
        self.community.save()
        self.assertEqual(self.community.original_name, "Foo")
        self.assertEqual(self.community.original_admin,
                         self.systers_user)

    def test_has_changed_name(self):
        """Test has_changed_name method of Community"""
        self.assertFalse(self.community.has_changed_name())
        self.community.name = "Bar"
        self.community.save()
        self.assertTrue(self.community.has_changed_name())

    def test_has_changed_admin(self):
        """Test has_changed_admin method of Community"""
        self.assertFalse(self.community.has_changed_admin())
        user = User.objects.create(username="bar", password="barfoo")
        systers_user2 = SystersUser.objects.get(user=user)
        self.community.admin = systers_user2
        self.community.save()
        self.assertTrue(self.community.has_changed_admin())

    def test_add_remove_member(self):
        """Test adding and removing Community members"""
        self.assertQuerysetEqual(self.community.members.all(), [])
        self.community.add_member(self.systers_user)
        self.community.save()
        self.assertSequenceEqual(self.community.members.all(),
                                 [self.systers_user])
        self.community.remove_member(self.systers_user)
        self.community.save()
        self.assertQuerysetEqual(self.community.members.all(), [])

    def test_get_fields(self):
        """Test getting Community fields"""
        fields = self.community.get_fields()
        self.assertTrue(len(fields), 12)
        self.assertTrue(fields[1], ('name', 'Foo'))

    def test_set_new_admin(self):
        """Test setting a new admin to a community"""
        post_save.connect(manage_community_groups, sender=Community,
                          dispatch_uid="manage_groups")
        post_delete.connect(remove_community_groups, sender=Community,
                            dispatch_uid="remove_groups")
        community = Community.objects.create(name="Bar", slug="bar",
                                             order=2, location=self.location,
                                             admin=self.systers_user)
        user = User.objects.create(username='bar', password='foobar')
        bar_systers_user = SystersUser.objects.get(user=user)
        status = community.set_new_admin(bar_systers_user)
        self.assertEqual(status, "not_member")

        community.add_member(bar_systers_user)
        community.save()
        status = community.set_new_admin(bar_systers_user)
        self.assertEqual(status, "ok")
        self.assertEqual(community.admin, bar_systers_user)
        admin_group = Group.objects.get(name=COMMUNITY_ADMIN.format("Bar"))
        self.assertSequenceEqual(bar_systers_user.user.groups.all(),
                                 [admin_group])
        self.assertSequenceEqual(self.systers_user.user.groups.all(), [])


class CommunityPageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_str(self):
        """Test CommunityPage object string representation"""
        page = CommunityPage(order=1, community=self.community, slug="bar",
                             title="Bar", author=self.systers_user)
        self.assertEqual(str(page), "Page Bar of Foo")
