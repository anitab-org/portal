from django.contrib.auth.models import User
from django.test import TestCase

from users.forms import UserForm, SystersUserForm
from users.models import SystersUser


class UserFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)

    def test_user_form(self):
        """Test the combined User and SystersUser form"""
        form = UserForm(instance=self.user)
        self.assertEqual(type(form.systers_user_form), SystersUserForm)
        data = {'first_name': 'Foo',
                'last_name': 'Bar',
                'blog_url': 'http://example.com/'}
        form = UserForm(data=data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.first_name, 'Foo')
        self.assertEqual(self.user.last_name, 'Bar')
        systers_user = SystersUser.objects.get(user=self.user)
        self.assertEqual(systers_user.blog_url, 'http://example.com/')
