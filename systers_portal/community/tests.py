from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from guardian.shortcuts import get_perms

from community.constants import COMMUNITY_ADMIN
from community.models import Community
from community.permissions import groups_templates, group_permissions
from community.signals import manage_community_groups
from community.utils import create_groups, assign_permissions, remove_groups
from users.models import SystersUser


class CommunityTestCase(TestCase):
    def setUp(self):
        post_save.disconnect(manage_community_groups, sender=Community,
                             dispatch_uid="create_groups")

    def test_create_groups(self):
        name = "Foo"
        groups = create_groups(name)
        expected_group_names = []
        for key, group_name in groups_templates.items():
            expected_group_names.append(group_name.format(name))
        group_names = []
        for group in groups:
            group_names.append(group.name)
        self.assertListEqual(expected_group_names, group_names)

        community_groups = Group.objects.filter(name__startswith=name)
        self.assertListEqual(list(community_groups), groups)

    def test_assign_permissions(self):
        User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get()
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             community_admin=systers_user)
        name = community.name
        groups = create_groups(name)
        assign_permissions(community, groups)
        for key, value in group_permissions.items():
            group = Group.objects.get(name=groups_templates[key].format(name))
            group_perms = [p.codename for p in
                           list(group.permissions.all())]
            group_perms += get_perms(group, community)
            self.assertItemsEqual(group_perms, value)

    def test_original_values(self):
        User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get()
        name = "Foo"
        community = Community.objects.create(name=name, slug="foo", order=1,
                                             community_admin=systers_user)
        self.assertEqual(community.original_name, name)
        self.assertEqual(community.community_admin, systers_user)
        community.name = "Bar"
        user = User.objects.create(username="bar", password="barfoo")
        systers_user2 = SystersUser.objects.get(user=user)
        community.community_admin = systers_user2
        community.save()
        self.assertEqual(community.original_name, name)
        self.assertEqual(community.original_community_admin, systers_user)

    def test_remove_groups(self):
        name = "Foo"
        create_groups(name)
        remove_groups(name)
        community_groups = Group.objects.filter(name__startswith=name)
        self.assertEqual(list(community_groups), [])

    def test_has_changed_name(self):
        User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get()
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             community_admin=systers_user)
        self.assertFalse(community.has_changed_name())
        community.name = "Bar"
        community.save()
        self.assertTrue(community.has_changed_name())

    def test_has_changed_community_admin(self):
        User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get()
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             community_admin=systers_user)
        self.assertFalse(community.has_changed_community_admin())
        user = User.objects.create(username="bar", password="barfoo")
        systers_user2 = SystersUser.objects.get(user=user)
        community.community_admin = systers_user2
        community.save()
        self.assertTrue(community.has_changed_community_admin())

    def test_manage_community_groups(self):
        post_save.connect(manage_community_groups, sender=Community,
                          dispatch_uid="create_groups")
        user1 = User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get()
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             community_admin=systers_user)
        groups_count = Group.objects.count()
        self.assertEqual(groups_count, 4)
        community_admin_group = Group.objects.get(
            name=COMMUNITY_ADMIN.format("Foo"))
        self.assertEqual(user1.groups.get(), community_admin_group)

        user2 = User.objects.create(username='bar', password='foobar')
        systers_user2 = SystersUser.objects.get(user=user2)
        community.name = "Bar"
        community.community_admin = systers_user2
        community.save()
        removed_groups_count = Group.objects.filter(
            name__startswith="Foo").count()
        self.assertEqual(removed_groups_count, 0)
        new_groups_count = Group.objects.filter(name__startswith="Bar").count()
        self.assertEqual(new_groups_count, 4)
        community_admin_group = Group.objects.get(
            name=COMMUNITY_ADMIN.format("Bar"))
        self.assertEqual(user2.groups.get(), community_admin_group)
        self.assertNotEqual(list(user1.groups.all()), [community_admin_group])

    def test_add_remove_member(self):
        User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get()
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             community_admin=systers_user)
        self.assertQuerysetEqual(community.members.all(), [])
        community.add_member(systers_user)
        self.assertEqual(list(community.members.all()), [systers_user])
        community.remove_member(systers_user)
        self.assertQuerysetEqual(community.members.all(), [])
