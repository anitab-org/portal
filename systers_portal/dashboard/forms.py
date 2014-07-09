from django import forms
from dashboard.models import SysterUser
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class SysterUserForm(forms.ModelForm):

    class Meta:
        model = SysterUser
        fields = ('country', 'blog_url', 'homepage_url', 'profile_picture')
