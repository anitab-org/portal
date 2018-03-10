from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import ChangePasswordForm
from django.core.exceptions import ValidationError

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
    class Meta:
        model = SystersUser
        fields = ('country', 'blog_url', 'homepage_url', 'profile_picture')


class SystersChangePasswordForm(ChangePasswordForm):
    # The clean_password1() method which checks that new password differs from the old one
    # is added to allauth ChangePasswordForm class.
    # So ChangePasswordForm class is derived.
    def __init__(self, *args, **kwargs):
        super(SystersChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        if self.cleaned_data["newpassword"] == self.cleaned_data.get("oldpassword", None):
            raise ValidationError("New password must differ from the old one.")
        return self.cleaned_data["new_password"]
