from django import forms
from dashboard.models import SysterUser, Community
from django.contrib.auth.models import User


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
