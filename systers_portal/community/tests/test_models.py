from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from community.models import Community, JoinRequest
from community.signals import manage_community_groups, remove_community_groups
from users.models import SystersUser


class CommunityModelTestCase(TestCase):
    def setUp(self):
        post_save.disconnect(manage_community_groups, sender=Community,
                             dispatch_uid="manage_groups")
        post_delete.disconnect(remove_community_groups, sender=Community,
                               dispatch_uid="remove_groups")
        User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_unicode(self):
        """Test Community object str/unicode representation"""
        self.assertEqual(unicode(self.community), "Foo")

    def test_original_values(self):
        """Test original community name and admin functioning"""
        self.assertEqual(self.community.original_name, "Foo")
        self.assertEqual(self.community.community_admin, self.systers_user)
        self.community.name = "Bar"
        user = User.objects.create(username="bar", password="barfoo")
        systers_user2 = SystersUser.objects.get(user=user)
        self.community.community_admin = systers_user2
        self.community.save()
        self.assertEqual(self.community.original_name, "Foo")
        self.assertEqual(self.community.original_community_admin,
                         self.systers_user)

    def test_has_changed_name(self):
        """Test has_changed_name method of Community"""
        self.assertFalse(self.community.has_changed_name())
        self.community.name = "Bar"
        self.community.save()
        self.assertTrue(self.community.has_changed_name())

    def test_has_changed_community_admin(self):
        """Test has_changed_community_admin method of Community"""
        self.assertFalse(self.community.has_changed_community_admin())
        user = User.objects.create(username="bar", password="barfoo")
        systers_user2 = SystersUser.objects.get(user=user)
        self.community.community_admin = systers_user2
        self.community.save()
        self.assertTrue(self.community.has_changed_community_admin())

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


class JoinRequestModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get()
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  community_admin=self.
                                                  systers_user)

    def test_unicode(self):
        """Test JoinRequest object str/unicode representation"""
        join_request = JoinRequest(user=self.systers_user,
                                   community=self.community)
        self.assertEqual(unicode(join_request),
                         "Join Request by foo - not approved")
        join_request.is_approved = True
        join_request.save()
        self.assertEqual(unicode(join_request),
                         "Join Request by foo - approved")
