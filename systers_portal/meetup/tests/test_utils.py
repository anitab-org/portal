from django.test import TestCase
from django.contrib.auth.models import Group, User
from guardian.shortcuts import get_perms
from cities_light.models import City, Country

from meetup.models import MeetupLocation
from meetup.permissions import groups_templates, group_permissions
from meetup.utils import (create_groups, assign_permissions, remove_groups,
                          get_groups)
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
        self.assertCountEqual(list(expected_group_names), group_names)

        meetup_location_groups = Group.objects.filter(name__startswith=name)
        self.assertCountEqual(meetup_location_groups, groups)

    def test_remove_groups(self):
        """Test the removal of groups according to a name"""
        name = "Foo"
        create_groups(name)
        remove_groups(name)
        meetup_location_groups = Group.objects.filter(name__startswith=name)
        self.assertEqual(list(meetup_location_groups), [])

    def test_get_groups(self):
        """Test getting groups according to meetup location name"""
        groups = get_groups("Foo")
        self.assertSequenceEqual(groups, [])
        name = "Bar"
        create_groups(name)
        meetup_location_groups = Group.objects.all()
        groups = get_groups("Bar")
        self.assertCountEqual(meetup_location_groups, groups)
        create_groups("New")
        groups = get_groups("Bar")
        self.assertCountEqual(meetup_location_groups, groups)

    def test_assign_permissions(self):
        """Test assignment of permissions to meetup location groups"""
        self.password = "foobar"
        user = User.objects.create_user(username='foo', password=self.password,
                                        email='user@test.com')
        systers_user = SystersUser.objects.get(user=user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Baz', display_name='Baz', country=country)
        meetup_location = MeetupLocation.objects.create(
            name="Foo Systers", slug="foo", location=location,
            description="It's a test meetup location", sponsors="BarBaz", leader=systers_user)
        name = meetup_location.name
        groups = create_groups(name)
        assign_permissions(meetup_location, groups)
        for key, value in group_permissions.items():
            group = Group.objects.get(name=groups_templates[key].format(name))
            group_perms = [p.codename for p in
                           list(group.permissions.all())]
            group_perms += get_perms(group, meetup_location)
            self.assertCountEqual(group_perms, value)
