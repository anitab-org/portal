from django import forms

from dashboard.models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        exclude = ('community', 'author')
