from django import forms
from django.contrib.auth.models import User

from common.helpers import SubmitCancelFormHelper
from users.models import SystersUser


class UserForm(forms.ModelForm):
    """User form combined with SystersUserForm"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        systers_user = SystersUser.objects.get(user=user)
        systers_user_kwargs = kwargs.copy()
        systers_user_kwargs['instance'] = systers_user
        self.systers_user_form = SystersUserForm(*args, **systers_user_kwargs)

        super(UserForm, self).__init__(*args, **kwargs)

        self.fields.update(self.systers_user_form.fields)
        self.initial.update(self.systers_user_form.initial)

        self.helper = SubmitCancelFormHelper(
            self, cancel_href="{{ systersuser.get_absolute_url }}")

    def save(self, *args, **kwargs):
        self.systers_user_form.save(*args, **kwargs)
        return super(UserForm, self).save(*args, **kwargs)


class SystersUserForm(forms.ModelForm):
    """Form for SystersUser model"""
    blog_url = forms.URLField(initial="http://",widget=forms.TextInput(attrs={'placeholder': 'Enter URL'}))
    homepage_url = forms.URLField(initial="http://",widget=forms.TextInput(attrs={'placeholder': 'Enter URL'}))
    class Meta:
        model = SystersUser
        fields = ('country', 'blog_url', 'homepage_url', 'profile_picture')
