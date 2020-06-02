from cities_light.models import Country, City
from django import forms
from django.contrib.auth.models import User
from django.test import TestCase

from community.models import Community
from membership.forms import TransferOwnershipForm
from users.models import SystersUser


class TransferOwnershipFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        country = Country.objects.create(name='Bar', continent='AS')
        location = City.objects.create(name='Foo', display_name='Foo',
                                       country=country)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1, location=location,
                                                  admin=self.systers_user)

    def test_transfer_ownership_form(self):
        """Test transferring ownership form"""
        form = TransferOwnershipForm(community=self.community)
        self.assertIsInstance(form.fields['new_admin'], forms.ChoiceField)
        self.assertSequenceEqual(form.fields['new_admin'].choices, [])

        bar_user = User.objects.create_user(username="bar", password="foobar")
        bar_systers_user = SystersUser.objects.get(user=bar_user)
        self.community.add_member(bar_systers_user)

        User.objects.create_user(username="new", password="foobar")

        form = TransferOwnershipForm(community=self.community)
        self.assertSequenceEqual(form.fields['new_admin'].choices,
                                 [(bar_user.id, "bar")])
