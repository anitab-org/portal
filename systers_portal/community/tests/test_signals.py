from cities_light.models import City, Country
from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save, post_delete

from community.constants import COMMUNITY_ADMIN
from community.models import Community
from community.signals import (manage_community_groups, remove_community_groups)
from users.models import SystersUser


class SignalsTestCase(TestCase):
    def setUp(self):
        post_save.connect(manage_community_groups, sender=Community,
                          dispatch_uid="manage_groups")
        post_delete.connect(remove_community_groups, sender=Community,
                            dispatch_uid="remove_groups")

    def test_manage_community_groups(self):
        """Test handling of operations required when saving a Community
        object"""
        user1 = User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get(user=user1)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=systers_user)
        groups_count = Group.objects.count()
        self.assertEqual(groups_count, 4)
        community_admin_group = Group.objects.get(
            name=COMMUNITY_ADMIN.format("Foo"))
        self.assertEqual(user1.groups.get(), community_admin_group)

        self.assertSequenceEqual(community.members.all(), [systers_user])

        user2 = User.objects.create(username='bar', password='foobar')
        systers_user2 = SystersUser.objects.get(user=user2)
        community.name = "Bar"
        community.admin = systers_user2
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
        self.assertCountEqual(Community.objects.get().members.all(),
                              [systers_user, systers_user2])

    def test_remove_community_groups(self):
        """Test the removal of groups when a community is deleted"""
        self.user = User.objects.create(username='foo', password='foobar')
        systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=systers_user)
        groups_count = Group.objects.count()
        self.assertEqual(groups_count, 4)
        community.delete()
        groups_count = Group.objects.count()
        self.assertEqual(groups_count, 0)
