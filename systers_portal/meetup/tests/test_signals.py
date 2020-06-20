from django.utils import timezone

from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save, post_delete, post_migrate
from cities_light.models import City, Country
from pinax.notifications.models import NoticeType

from meetup.models import Meetup
from users.models import SystersUser

from meetup.signals import manage_meetup_groups, remove_meetup_groups, create_notice_types


class SignalsTestCase(TestCase):
    def setUp(self):
        post_save.connect(manage_meetup_groups, sender=Meetup,
                          dispatch_uid="manage_groups")
        post_delete.connect(remove_meetup_groups, sender=Meetup,
                            dispatch_uid="remove_groups")
        post_migrate.connect(create_notice_types, dispatch_uid="create_notice_types")
        self.password = "foobar"

    def test_manage_meetup_location_groups(self):
        """Test addition of groups when saving a Meetup Location object"""
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
        self.assertEqual("Foo Bar Baz", meetup.title)
        groups_count = Group.objects.count()
        self.assertEqual(groups_count, 3)

    def test_remove_community_groups(self):
        """Test the removal of groups when a Meetup Location is deleted"""
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
        groups_count = Group.objects.count()
        self.assertEqual(groups_count, 3)
        meetup.delete()
        groups_count = Group.objects.count()
        self.assertEqual(groups_count, 0)

    def test_create_notice_types(self):
        """Test creation of notice types"""
        notice_types = NoticeType.objects.all()
        self.assertEqual(len(notice_types), 4)
        new_meetup = NoticeType.objects.get(label="new_meetup")
        self.assertEqual(new_meetup.display, "New Meetup")
        new_support_request = NoticeType.objects.get(label="new_support_request")
        self.assertEqual(new_support_request.display, "New Support Request")
        support_request_approved = NoticeType.objects.get(label="support_request_approved")
        self.assertEqual(support_request_approved.display, "Support Request Approved")
        new_meetup_request = NoticeType.objects.get(label="new_meetup_request")
        self.assertEqual(new_meetup_request.display, "New Meetup Request")
