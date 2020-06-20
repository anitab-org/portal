from django.test import TestCase
from django.contrib.auth.models import Group, User
from guardian.shortcuts import get_perms
from cities_light.models import City, Country

from django.utils import timezone
from meetup.models import Meetup
from meetup.permissions import groups_templates, group_permissions
from meetup.utils import (create_groups, assign_permissions, remove_groups)
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

        meetup_groups = Group.objects.filter(name__startswith=name)
        self.assertCountEqual(meetup_groups, groups)

    def test_remove_groups(self):
        """Test the removal of groups according to a name"""
        name = "Foo"
        create_groups(name)
        remove_groups(name)
        meetup_groups = Group.objects.filter(name__startswith=name)
        self.assertEqual(list(meetup_groups), [])

    def test_assign_permissions(self):
        """Test assignment of permissions to meetup location groups"""
        self.password = "foobar"
        user = User.objects.create_user(username='foo', password=self.password,
                                        email='user@test.com')
        systers_user = SystersUser.objects.get(user=user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Baz', display_name='Baz', country=country)
        meetup = Meetup.objects.create(title='Foo Bar Baz', slug='foo-bar-baz',
                                       date=timezone.now().date(),
                                       time=timezone.now().time(),
                                       description='This is test Meetup',
                                       meetup_location=location,
                                       created_by=systers_user,
                                       leader=systers_user,
                                       last_updated=timezone.now())
        title = meetup.title
        groups = create_groups(title)
        assign_permissions(meetup, groups)
        for key, value in group_permissions.items():
            group = Group.objects.get(name=groups_templates[key].format(title))
            group_perms = [p.codename for p in
                           list(group.permissions.all())]
            group_perms += get_perms(group, meetup)
            self.assertCountEqual(group_perms, value)
