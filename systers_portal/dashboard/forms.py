from django import forms
from django.contrib.auth.models import User
from django.forms.models import model_to_dict, fields_for_model

from dashboard.models import SysterUser


class UserForm(forms.ModelForm):
    """Combined Form for SysterUser and User"""
    def __init__(self, instance=None, *args, **kwargs):
        _fields = ('country', 'blog_url', 'homepage_url', 'profile_picture')
	if instance is not None:
            _initial = model_to_dict(instance.systeruser, _fields)
        else:
            _initial = {}
        super(UserForm, self).__init__(
            initial=_initial,
            instance=instance,
            *args,
            **kwargs)
        self.fields.update(fields_for_model(SysterUser, _fields))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def save(self, *args, **kwargs):
        systeruser = self.instance.systeruser
        for field in self.cleaned_data:
            try:
                setattr(systeruser, field, self.cleaned_data[field])
            except AttributeError:
                pass
        systeruser.save()
        user = super(UserForm, self).save(*args, **kwargs)
        return user
