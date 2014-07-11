from django import forms

from dashboard.models import News


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        exclude = ('community', 'author')
