from django.test import TestCase
from django.contrib.auth.models import Group, User
from guardian.shortcuts import get_perms

from community.models import Community
from community.permissions import groups_templates, group_permissions
from community.utils import (create_groups, assign_permissions, remove_groups,
                             rename_groups, get_groups)
from users.models import SystersUser


class UtilsTestCase(TestCase):
    def test_create_groups(self):
        """Test the creation of groups according to a name"""
        name = "Foo"
        groups = create_groups(name)
        expected_group_names = []
        for key, group_name in groups_templates.items():
            expected_group_names.append(group_name.format(name))
        group_names = []
        for group in groups:
            group_names.append(group.name)
        self.assertItemsEqual(expected_group_names, group_names)

        community_groups = Group.objects.filter(name__startswith=name)
        self.assertItemsEqual(list(community_groups), groups)

    def test_remove_groups(self):
        """Test the removal of groups according to a name"""
        name = "Foo"
        create_groups(name)
        remove_groups(name)
        community_groups = Group.objects.filter(name__startswith=name)
        self.assertEqual(list(community_groups), [])

    def test_get_groups(self):
        """Test getting groups according to community name"""
        groups = get_groups("Foo")
        self.assertSequenceEqual(groups, [])
        name = "Bar"
        create_groups(name)
        community_groups = Group.objects.all()
        groups = get_groups("Bar")
        self.assertItemsEqual(community_groups, groups)
        create_groups("New")
        groups = get_groups("Bar")
        self.assertItemsEqual(community_groups, groups)

    def test_rename_groups(self):
        """Test the renaming of groups according to a new name"""
        old_name = "Foo"
        new_name = "Bar"
        create_groups(old_name)
        groups = rename_groups(old_name, new_name)
        expected_group_names = []
        for key, group_name in groups_templates.items():
            expected_group_names.append(group_name.format(new_name))
        group_names = []
        for group in groups:
            group_names.append(group.name)
        self.assertItemsEqual(expected_group_names, group_names)

        community_groups = Group.objects.filter(name__startswith=new_name)
        self.assertItemsEqual(community_groups, groups)
        old_community_groups = Group.objects.filter(name__startswith=old_name)
        self.assertSequenceEqual(old_community_groups, [])

    def test_assign_permissions(self):
        """Test assignment of permissions to community groups"""
        User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get()
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             admin=systers_user)
        name = community.name
        groups = create_groups(name)
        assign_permissions(community, groups)
        for key, value in group_permissions.items():
            group = Group.objects.get(name=groups_templates[key].format(name))
            group_perms = [p.codename for p in
                           list(group.permissions.all())]
            group_perms += get_perms(group, community)
            self.assertItemsEqual(group_perms, value)
