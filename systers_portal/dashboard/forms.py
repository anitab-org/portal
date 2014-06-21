from django import forms
from dashboard.models import SysterUser, Community
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SysterUserForm(forms.ModelForm):

    class Meta:
        model = SysterUser
        fields = ('country', 'blog_url', 'homepage_url', 'profile_picture')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


