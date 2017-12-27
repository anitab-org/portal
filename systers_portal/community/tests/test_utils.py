from django.test import TestCase
from django.contrib.auth.models import Group, User
from guardian.shortcuts import get_perms

from community.models import Community, RequestCommunity
from community.permissions import groups_templates, group_permissions, requestor_group_templates,\
    requestor_group_permissions
from community.utils import (
    create_groups, assign_permissions, remove_groups, rename_groups, get_groups)
from users.models import SystersUser


class UtilsTestCase(TestCase):
    def test_create_groups(self):
        """Test the creation of groups according to a name"""
        name = "Foo"
        groups = create_groups(name, groups_templates)
        expected_group_names = []
        for key, group_name in groups_templates.items():
            expected_group_names.append(group_name.format(name))
        group_names = []
        for group in groups:
            group_names.append(group.name)
        self.assertCountEqual(list(expected_group_names), group_names)

        community_groups = Group.objects.filter(name__startswith=name)
        self.assertCountEqual(community_groups, groups)

    def test_remove_groups(self):
        """Test the removal of groups according to a name"""
        name = "Foo"
        create_groups(name, groups_templates)
        remove_groups(name)
        community_groups = Group.objects.filter(name__startswith=name)
        self.assertEqual(list(community_groups), [])

        create_groups(name, requestor_group_templates)
        remove_groups(name)
        community_request_groups = Group.objects.filter(name__startswith=name)
        self.assertEqual(list(community_request_groups), [])

    def test_get_groups(self):
        """Test getting groups according to community name"""
        groups = get_groups("Foo")
        self.assertSequenceEqual(groups, [])
        name = "Bar"
        create_groups(name, groups_templates)
        community_groups = Group.objects.all()
        groups = get_groups("Bar")
        self.assertCountEqual(community_groups, groups)
        create_groups("New", groups_templates)
        groups = get_groups("Bar")
        self.assertCountEqual(community_groups, groups)

    def test_rename_groups(self):
        """Test the renaming of groups according to a new name"""
        old_name = "Foo"
        new_name = "Bar"
        create_groups(old_name, groups_templates)
        groups = rename_groups(old_name, new_name)
        expected_group_names = []
        for key, group_name in groups_templates.items():
            expected_group_names.append(group_name.format(new_name))
        group_names = []
        for group in groups:
            group_names.append(group.name)
        self.assertCountEqual(expected_group_names, group_names)

        community_groups = Group.objects.filter(name__startswith=new_name)
        self.assertCountEqual(community_groups, groups)
        old_community_groups = Group.objects.filter(name__startswith=old_name)
        self.assertSequenceEqual(old_community_groups, [])

    def test_assign_permissions(self):
        """Test assignment of permissions to community and request community groups"""
        self.user = User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get(user=self.user)
        community = Community.objects.create(name="Foo", slug="foo", order=1,
                                             admin=systers_user)
        name = community.name
        groups = create_groups(name, groups_templates)
        assign_permissions(community, groups,
                           groups_templates, group_permissions)
        for key, value in group_permissions.items():
            group = Group.objects.get(name=groups_templates[key].format(name))
            group_perms = [p.codename for p in
                           list(group.permissions.all())]
            group_perms += get_perms(group, community)
            self.assertCountEqual(group_perms, value)

        community_request = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, is_member='Yes', type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=systers_user)
        name = community_request.name
        groups = create_groups(name, requestor_group_templates)
        assign_permissions(community_request, groups,
                           requestor_group_templates, requestor_group_permissions)
        for key, value in requestor_group_permissions.items():
            group = Group.objects.get(
                name=requestor_group_templates[key].format(name))
            group_perms = [p.codename for p in
                           list(group.permissions.all())]
            group_perms += get_perms(group, community_request)
            self.assertCountEqual(group_perms, value)
